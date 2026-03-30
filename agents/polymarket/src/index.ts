/**
 * KairuAI · Polymarket Agent
 * Monitor prediction markets, fetch odds, and surface high-value opportunities.
 */

import "dotenv/config";

const CLOB_API = "https://clob.polymarket.com";
const GAMMA_API = "https://gamma-api.polymarket.com";

interface Market {
  condition_id: string;
  question: string;
  end_date_iso: string;
  active: boolean;
  volume: string;
  tokens: Array<{ token_id: string; outcome: string; price: number }>;
}

interface MarketSummary {
  question: string;
  endDate: string;
  volume: number;
  yesPrice: number;
  noPrice: number;
  spread: number;
  impliedYesPct: number;
}

async function fetchActiveMarkets(limit: number = 20): Promise<Market[]> {
  const url = `${GAMMA_API}/markets?active=true&closed=false&limit=${limit}&order=volume&ascending=false`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Gamma API error: ${res.statusText}`);
  return res.json() as Promise<Market[]>;
}

async function fetchMarketById(conditionId: string): Promise<Market> {
  const res = await fetch(`${CLOB_API}/markets/${conditionId}`);
  if (!res.ok) throw new Error(`CLOB API error: ${res.statusText}`);
  return res.json() as Promise<Market>;
}

function parseMarket(market: Market): MarketSummary {
  const yes = market.tokens.find(t => t.outcome.toLowerCase() === "yes");
  const no  = market.tokens.find(t => t.outcome.toLowerCase() === "no");

  const yesPrice = yes?.price ?? 0;
  const noPrice  = no?.price ?? 0;
  const spread   = Math.abs(yesPrice + noPrice - 1);

  return {
    question:       market.question,
    endDate:        market.end_date_iso?.slice(0, 10) ?? "N/A",
    volume:         parseFloat(market.volume ?? "0"),
    yesPrice,
    noPrice,
    spread:         parseFloat(spread.toFixed(4)),
    impliedYesPct:  parseFloat((yesPrice * 100).toFixed(1)),
  };
}

function findOpportunities(markets: MarketSummary[]): MarketSummary[] {
  // Surface markets with high volume + significant price skew (potential mispricing)
  return markets
    .filter(m => m.volume > 10_000 && (m.yesPrice < 0.15 || m.yesPrice > 0.85))
    .sort((a, b) => b.volume - a.volume)
    .slice(0, 5);
}

function printMarket(m: MarketSummary, idx: number): void {
  const bar = "█".repeat(Math.round(m.impliedYesPct / 5));
  const empty = "░".repeat(20 - Math.round(m.impliedYesPct / 5));
  console.log(`\n  [${idx + 1}] ${m.question.slice(0, 72)}...`);
  console.log(`      End: ${m.endDate} | Vol: $${(m.volume / 1000).toFixed(0)}K`);
  console.log(`      YES: ${(m.yesPrice * 100).toFixed(1)}%  NO: ${(m.noPrice * 100).toFixed(1)}%`);
  console.log(`      [${bar}${empty}] ${m.impliedYesPct}%`);
}

async function main() {
  console.log("\n  KairuAI · Polymarket Agent");
  console.log("  Prediction Market Intelligence\n");

  let markets: Market[];
  try {
    console.log("  Fetching top markets by volume...");
    markets = await fetchActiveMarkets(30);
    console.log(`  ✓ Loaded ${markets.length} active markets`);
  } catch (e) {
    console.error(`  ✗ Failed to fetch markets: ${e}`);
    process.exit(1);
  }

  const summaries = markets.map(parseMarket);

  // Top 5 by volume
  console.log("\n  ─── Top Markets by Volume ───");
  summaries
    .sort((a, b) => b.volume - a.volume)
    .slice(0, 5)
    .forEach(printMarket);

  // Opportunities (high confidence + high volume)
  const opps = findOpportunities(summaries);
  if (opps.length > 0) {
    console.log("\n  ─── High-Confidence Opportunities ───");
    console.log("  (High volume + price > 85% or < 15% — strong consensus)");
    opps.forEach(printMarket);
  }

  console.log("\n  ─── Market Stats ───");
  const totalVol = summaries.reduce((s, m) => s + m.volume, 0);
  const avgYes   = summaries.reduce((s, m) => s + m.yesPrice, 0) / summaries.length;
  console.log(`  Total volume: $${(totalVol / 1_000_000).toFixed(2)}M`);
  console.log(`  Avg YES price: ${(avgYes * 100).toFixed(1)}%`);
  console.log(`  Markets analyzed: ${summaries.length}\n`);
}

export { fetchActiveMarkets, fetchMarketById, parseMarket, findOpportunities };

main().catch(console.error);
