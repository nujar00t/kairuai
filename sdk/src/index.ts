/**
 * KairuAI · SDK
 * TypeScript client for interacting with KairuAI agents programmatically.
 */

export interface KairuConfig {
  rpcUrl?: string;
  slippageBps?: number;
}

export interface PriceData {
  symbol: string;
  price: number;
  timestamp: number;
}

export interface MarketOpportunity {
  question: string;
  yesPrice: number;
  noPrice: number;
  volume: number;
  impliedYesPct: number;
}

export interface TradeSignal {
  action: "BUY" | "SELL" | "HOLD";
  confidence: number;
  reason: string;
  token?: string;
}

// Fetch token price from Jupiter
export async function getPrice(mint: string): Promise<PriceData> {
  const res = await fetch(`https://price.jup.ag/v6/price?ids=${mint}`);
  if (!res.ok) throw new Error(`Price fetch failed: ${res.statusText}`);
  const data = (await res.json()) as { data: Record<string, { price: number }> };
  return {
    symbol: mint,
    price: data.data[mint]?.price ?? 0,
    timestamp: Date.now(),
  };
}

// Fetch top Polymarket markets
export async function getMarkets(limit = 10): Promise<MarketOpportunity[]> {
  const url = `https://gamma-api.polymarket.com/markets?active=true&closed=false&limit=${limit}&order=volume&ascending=false`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Markets fetch failed: ${res.statusText}`);
  const markets = (await res.json()) as Array<{
    question: string;
    volume: string;
    tokens: Array<{ outcome: string; price: number }>;
  }>;

  return markets.map(m => {
    const yes = m.tokens.find(t => t.outcome.toLowerCase() === "yes");
    const no  = m.tokens.find(t => t.outcome.toLowerCase() === "no");
    return {
      question:      m.question,
      yesPrice:      yes?.price ?? 0,
      noPrice:       no?.price ?? 0,
      volume:        parseFloat(m.volume ?? "0"),
      impliedYesPct: parseFloat(((yes?.price ?? 0) * 100).toFixed(1)),
    };
  });
}

// Simple signal generator based on price momentum
export function generateSignal(prices: number[]): TradeSignal {
  if (prices.length < 3) {
    return { action: "HOLD", confidence: 0, reason: "Insufficient price data" };
  }

  const latest  = prices[prices.length - 1];
  const prev    = prices[prices.length - 2];
  const oldest  = prices[0];
  const change  = (latest - prev) / prev;
  const overall = (latest - oldest) / oldest;

  if (change > 0.02 && overall > 0.05) {
    return {
      action: "BUY",
      confidence: Math.min(Math.abs(overall) * 100, 90),
      reason: `Upward momentum: +${(change * 100).toFixed(2)}% recent, +${(overall * 100).toFixed(2)}% overall`,
    };
  } else if (change < -0.02 && overall < -0.05) {
    return {
      action: "SELL",
      confidence: Math.min(Math.abs(overall) * 100, 90),
      reason: `Downward momentum: ${(change * 100).toFixed(2)}% recent, ${(overall * 100).toFixed(2)}% overall`,
    };
  }

  return {
    action: "HOLD",
    confidence: 50,
    reason: "No clear momentum signal",
  };
}
