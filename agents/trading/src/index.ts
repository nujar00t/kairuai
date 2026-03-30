/**
 * KairuAI · Trading Agent
 * Execute token swaps on Solana via Jupiter Aggregator.
 */

import { Connection, Keypair, PublicKey, VersionedTransaction } from "@solana/web3.js";
import "dotenv/config";

const RPC_URL = process.env.SOLANA_RPC_URL ?? "https://api.mainnet-beta.solana.com";
const JUPITER_QUOTE_API = "https://quote-api.jup.ag/v6";

// Token mint addresses
const TOKENS: Record<string, string> = {
  SOL:  "So11111111111111111111111111111111111111112",
  USDC: "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
};

interface QuoteResponse {
  inputMint: string;
  outputMint: string;
  inAmount: string;
  outAmount: string;
  priceImpactPct: string;
  routePlan: unknown[];
}

async function getQuote(
  inputMint: string,
  outputMint: string,
  amount: number,
  slippageBps: number = 50
): Promise<QuoteResponse> {
  const url = `${JUPITER_QUOTE_API}/quote?inputMint=${inputMint}&outputMint=${outputMint}&amount=${amount}&slippageBps=${slippageBps}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Quote API error: ${res.statusText}`);
  return res.json() as Promise<QuoteResponse>;
}

async function executeSwap(
  wallet: Keypair,
  quote: QuoteResponse
): Promise<string> {
  const connection = new Connection(RPC_URL, "confirmed");

  const swapRes = await fetch(`${JUPITER_QUOTE_API}/swap`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      quoteResponse: quote,
      userPublicKey: wallet.publicKey.toString(),
      wrapAndUnwrapSol: true,
      dynamicComputeUnitLimit: true,
      prioritizationFeeLamports: "auto",
    }),
  });

  if (!swapRes.ok) throw new Error(`Swap API error: ${swapRes.statusText}`);
  const { swapTransaction } = (await swapRes.json()) as { swapTransaction: string };

  const txBuf = Buffer.from(swapTransaction, "base64");
  const tx = VersionedTransaction.deserialize(txBuf);
  tx.sign([wallet]);

  const sig = await connection.sendRawTransaction(tx.serialize(), {
    skipPreflight: false,
    maxRetries: 3,
  });

  await connection.confirmTransaction(sig, "confirmed");
  return sig;
}

async function getTokenPrice(mint: string): Promise<number> {
  const url = `https://price.jup.ag/v6/price?ids=${mint}`;
  const res = await fetch(url);
  if (!res.ok) return 0;
  const data = (await res.json()) as { data: Record<string, { price: number }> };
  return data.data[mint]?.price ?? 0;
}

async function main() {
  console.log("\n  KairuAI · Trading Agent");
  console.log("  Solana DEX via Jupiter Aggregator\n");

  const connection = new Connection(RPC_URL, "confirmed");

  // Check RPC connection
  try {
    const slot = await connection.getSlot();
    console.log(`  ✓ Connected to Solana · slot ${slot}`);
  } catch (e) {
    console.error(`  ✗ RPC connection failed: ${e}`);
    process.exit(1);
  }

  // Show current prices
  console.log("\n  Current Prices:");
  for (const [symbol, mint] of Object.entries(TOKENS)) {
    const price = await getTokenPrice(mint);
    console.log(`    ${symbol.padEnd(6)} $${price.toFixed(4)}`);
  }

  // Demo: get a quote for 0.1 SOL → USDC
  const amountLamports = 0.1 * 1_000_000_000;
  console.log("\n  Sample Quote: 0.1 SOL → USDC");
  try {
    const quote = await getQuote(TOKENS.SOL, TOKENS.USDC, amountLamports);
    const outUsdc = Number(quote.outAmount) / 1_000_000;
    const impact = parseFloat(quote.priceImpactPct).toFixed(4);
    console.log(`    Out: ${outUsdc.toFixed(2)} USDC`);
    console.log(`    Price impact: ${impact}%`);
    console.log(`    Routes: ${quote.routePlan.length}`);
  } catch (e) {
    console.error(`  Quote error: ${e}`);
  }

  console.log("\n  To execute a real swap, call executeSwap() with your Keypair.");
  console.log("  WARNING: Set SOLANA_PRIVATE_KEY in .env before trading.\n");
}

export { getQuote, executeSwap, getTokenPrice, TOKENS };

main().catch(console.error);
