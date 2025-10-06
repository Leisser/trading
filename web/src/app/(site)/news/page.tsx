import { Metadata } from "next";
import { Icon } from "@iconify/react";
import Link from "next/link";
import Image from "next/image";

export const metadata: Metadata = {
  title: "Latest News | Fluxor",
  description: "Stay updated with the latest cryptocurrency news and market insights from Fluxor",
};

// News data with detailed content
const newsData = [
  {
    id: 1,
    category: "Market Analysis",
    title: "Bitcoin Reaches New All-Time High Amid Institutional Adoption",
    summary: "Bitcoin soars to record levels, fueled by corporate balance sheet adoption.",
    read_time: 5,
    date: "2025-03-22",
    body: "Bitcoin's latest ascent to a fresh all-time high marks yet another chapter in its volatile evolution. This rally is being driven by deeper structural shifts, not just speculative momentum.\n\n- 2017 Peak & Crash: Bitcoin soared past $19,000 before collapsing to below $4,000. That cycle revealed hype dangers.\n- 2020–2021 Institutional Influx: Companies like MicroStrategy added Bitcoin to their balance sheets; Tesla bought $1.5B.\n- 2024 Regulatory Clarity: Clearer crypto laws in the US and EU reduced legal risk.\n- 2025 Surge: ETFs, sovereign wealth funds, and hedge funds are returning. Analysts see a new paradigm where price floors are higher and downside is muted.",
    image_url: "https://images.unsplash.com/photo-1518546305927-5a555bb7020d?w=800"
  },
  {
    id: 2,
    category: "Technology",
    title: "Ethereum 2.0 Upgrade Shows Promising Results",
    summary: "Ethereum's network upgrades boost transaction speed and reduce energy consumption.",
    read_time: 4,
    date: "2023-10-05",
    body: "Ethereum was once criticized for scalability issues and high gas fees. Its transition to Ethereum 2.0 is delivering meaningful change.\n\n- 2016 Origins & DAO Hack: Forced a chain split, teaching governance and consensus lessons.\n- 2017 ICO Boom & Gas Spikes: Gas fees skyrocketed, showing scalability limits.\n- 2022–23 Upgrades: Merge shifted Ethereum to Proof of Stake, slashing energy usage. Sharding and data improvements are underway.\n- 2023 Real Results: Gas fees dropped, block times smoothed, developers returned, making dApps practical again.",
    image_url: "https://images.unsplash.com/photo-1622630998477-20aa696ecb05?w=800"
  },
  {
    id: 3,
    category: "Regulation",
    title: "Regulatory Clarity Boosts Crypto Market Confidence",
    summary: "New laws and guidelines reduce investor risk, fueling crypto growth.",
    read_time: 6,
    date: "2024-08-13",
    body: "Regulation has been both crypto's enemy and savior. This new wave of clarity marks a turning point.\n\n- 2013–2014 Wild West: Minimal oversight; Mt. Gox and hacks highlighted risks.\n- 2017 ICO Crackdowns: SEC enforcement cooled speculation.\n- 2021–2023 Legal Battles: SEC vs Ripple, Coinbase scrutiny kept institutions cautious.\n- 2024 Clarity: Legislation and frameworks now provide compliance paths, unlocking institutional capital and user trust.",
    image_url: "https://images.unsplash.com/photo-1589923188900-85dae523342b?w=800"
  },
  {
    id: 4,
    category: "DeFi",
    title: "DeFi Protocols See Record TVL Growth",
    summary: "Total Value Locked in decentralized finance protocols hits new milestones.",
    read_time: 3,
    date: "2021-11-09",
    body: "Decentralized finance started as an experiment but has grown rapidly.\n\n- 2018 DeFi 1.0: MakerDAO, Compound enabled algorithmic lending.\n- 2020 Yield Farming: Yearn Finance, SushiSwap drove explosive interest.\n- 2021 Overleveraging: TVL peaked above $100B; risks surfaced.\n- Today: DeFi 2.0 focuses on resilience, dynamic yields, cross-chain liquidity, and institutional integration.",
    image_url: "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=800"
  },
  {
    id: 5,
    category: "CBDC",
    title: "Central Bank Digital Currencies Gain Momentum",
    summary: "CBDC pilots accelerate globally, reshaping monetary systems.",
    read_time: 7,
    date: "2025-01-15",
    body: "CBDCs are moving from theory to reality.\n\n- 1980–2000s Digital Banking: Money became digital, laying the groundwork.\n- 2014 China Digital Yuan: Early R&D and city-level pilot programs.\n- 2021–2022 Global Studies: ECB, Caribbean, and African trials.\n- 2025 Deployment: Retail interfaces exist, cross-border experiments underway, showing CBDCs can coexist with cryptocurrencies.",
    image_url: "https://images.unsplash.com/photo-1580519542036-c47de6196ba5?w=800"
  },
  {
    id: 6,
    category: "NFT",
    title: "NFT Market Shows Signs of Recovery",
    summary: "NFT adoption rebounds with utility-driven projects after a market slowdown.",
    read_time: 4,
    date: "2024-04-20",
    body: "NFTs went through hype, crash, and are now returning with stronger fundamentals.\n\n- 2017–2018 CryptoKitties: Early experiments, high gas fees.\n- 2021 Boom: Speculative sales exploded.\n- 2022–2023 Chill: Many projects lost value.\n- 2024 Renewal: Utility-focused NFTs in gaming, identity, and real-world experiences emerge, creating sustainable market activity.",
    image_url: "https://stormgain.com/sites/default/files/2022-04/best-nft-coins-list-main.jpg"
  },
  {
    id: 7,
    category: "Security",
    title: "Major DeFi Protocol Hacked for $200M in Sophisticated Attack",
    summary: "Hackers exploit smart contract vulnerability, raising security concerns across DeFi ecosystem.",
    read_time: 5,
    date: "2024-09-18",
    body: "A major DeFi protocol suffered one of the largest hacks in crypto history when attackers exploited a previously unknown vulnerability in their cross-chain bridge contract.\n\n- Attack Details: Hackers drained $200M in multiple tokens over several hours before the protocol team could respond.\n- Root Cause: A logic error in the bridge contract's validation mechanism allowed unauthorized withdrawals.\n- Industry Response: Multiple protocols paused operations to audit similar code patterns.\n- Recovery Efforts: The protocol offered a 10% bounty for return of funds and is working with authorities to trace the stolen assets through blockchain forensics.",
    image_url: "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=800"
  },
  {
    id: 8,
    category: "Altcoins",
    title: "Solana Network Achieves 400,000 TPS in Breakthrough Test",
    summary: "Solana demonstrates unprecedented transaction throughput, challenging Ethereum's dominance.",
    read_time: 4,
    date: "2024-11-25",
    body: "Solana's latest testnet achieved 400,000 transactions per second, showcasing the blockchain's technical capabilities and positioning it as a serious competitor in the layer-1 race.\n\n- Performance Metrics: The test sustained high throughput for over 12 hours with minimal degradation.\n- Technical Innovation: New consensus optimizations and parallel transaction processing drove the improvement.\n- Developer Interest: Major projects are migrating from Ethereum due to lower costs and higher speed.\n- Challenges Ahead: Network stability remains a concern after several high-profile outages in 2023-2024.",
    image_url: "https://images.unsplash.com/photo-1639762681057-408e52192e55?w=800"
  },
  {
    id: 9,
    category: "Enterprise",
    title: "Fortune 500 Companies Embrace Blockchain for Supply Chain",
    summary: "Major corporations integrate blockchain technology to improve transparency and efficiency.",
    read_time: 6,
    date: "2024-12-03",
    body: "Enterprise blockchain adoption accelerates as Fortune 500 companies deploy real-world solutions for supply chain management, moving beyond pilot programs to production systems.\n\n- Use Cases: Track-and-trace for pharmaceuticals, food safety, luxury goods authentication, and carbon credit tracking.\n- Key Players: Walmart, IBM, Maersk, and Nestle lead enterprise adoption.\n- Technology: Private and permissioned blockchains dominate, with some hybrid public-private architectures emerging.\n- Benefits: 30% reduction in documentation costs, 50% faster dispute resolution, and improved compliance reporting.",
    image_url: "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800"
  },
  {
    id: 10,
    category: "Layer 2",
    title: "Ethereum Layer 2 Solutions Process More Transactions Than Mainnet",
    summary: "Rollups and sidechains handle majority of Ethereum activity, reducing costs dramatically.",
    read_time: 5,
    date: "2025-02-08",
    body: "Layer 2 scaling solutions have matured to the point where they now process more daily transactions than Ethereum mainnet, marking a significant milestone in blockchain scalability.\n\n- Leading Solutions: Arbitrum, Optimism, Polygon, and zkSync dominate the L2 landscape.\n- Cost Savings: Transaction fees on L2s average $0.10-$0.50 compared to $2-$20 on mainnet.\n- Security Model: All major L2s inherit Ethereum's security while offering 10-100x throughput improvements.\n- Future Outlook: Proto-danksharding in 2025 will further reduce L2 costs by 10x through data availability improvements.",
    image_url: "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=800"
  },
  {
    id: 11,
    category: "Gaming",
    title: "Web3 Gaming Market Surpasses $10B Valuation",
    summary: "Blockchain gaming evolves beyond play-to-earn with focus on actual gameplay quality.",
    read_time: 4,
    date: "2024-10-15",
    body: "Web3 gaming has matured significantly, moving past the speculative play-to-earn models to deliver actual entertainment value with sustainable tokenomics.\n\n- Market Growth: $10B+ invested in web3 gaming companies in 2024.\n- Top Games: Immutable X titles, Axie Infinity's evolution, and new AAA blockchain games attract millions of players.\n- Key Innovation: Asset interoperability between games creates true digital ownership.\n- Challenges: Balancing fun gameplay with economic incentives remains difficult; many projects still fail to retain players.",
    image_url: "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=800"
  },
  {
    id: 12,
    category: "Stablecoins",
    title: "Stablecoin Market Cap Exceeds $200B as Adoption Accelerates",
    summary: "USD-pegged cryptocurrencies become preferred medium for cross-border payments.",
    read_time: 5,
    date: "2025-03-01",
    body: "Stablecoins have emerged as the killer app for crypto, with market capitalization surpassing $200B as businesses and individuals use them for payments, remittances, and savings.\n\n- Market Leaders: USDT dominates with $120B, USDC follows with $50B, and algorithmic stablecoins hold smaller shares.\n- Use Cases: International remittances see 90% cost reduction, merchants avoid credit card fees, and emerging markets use stablecoins as dollar alternatives.\n- Regulatory Progress: Clear frameworks in EU and selective US states enable compliant stablecoin operations.\n- Competition: Traditional payment companies like PayPal and Visa launch their own stablecoin products.",
    image_url: "https://images.unsplash.com/photo-1621504450181-5d356f61d307?w=800"
  },
  {
    id: 13,
    category: "Privacy",
    title: "Privacy Coins Face Increased Scrutiny from Regulators",
    summary: "Governments crack down on anonymous cryptocurrencies, citing money laundering concerns.",
    read_time: 6,
    date: "2024-07-22",
    body: "Privacy-focused cryptocurrencies face mounting pressure as regulators worldwide implement stricter controls, leading to delistings from major exchanges.\n\n- Affected Coins: Monero, Zcash, and Dash face restrictions in multiple jurisdictions.\n- Regulatory Stance: EU's MiCA regulations and US Treasury sanctions target privacy-enhancing technologies.\n- Industry Response: Privacy advocates argue for fundamental right to financial privacy while acknowledging compliance needs.\n- Technical Evolution: New privacy solutions focus on selective disclosure and regulatory-compliant anonymity.",
    image_url: "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?w=800"
  },
  {
    id: 14,
    category: "Mining",
    title: "Bitcoin Mining Shifts to Renewable Energy Sources",
    summary: "Over 60% of mining operations now powered by sustainable energy, industry reports show.",
    read_time: 5,
    date: "2024-06-30",
    body: "Bitcoin mining undergoes green revolution as miners increasingly tap into renewable energy sources, addressing environmental criticism.\n\n- Energy Mix: Hydroelectric (35%), solar (15%), wind (10%), and other renewables power majority of mining.\n- Geographic Shift: Mining moves from coal-heavy regions to areas with abundant renewable energy like Iceland, Norway, and Texas.\n- Innovation: Miners partner with renewable energy developers to monetize stranded energy and stabilize power grids.\n- Economic Benefits: Low-cost renewable energy makes mining more profitable while reducing carbon footprint by 50% since 2020.",
    image_url: "https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=800"
  },
  {
    id: 15,
    category: "Tokenization",
    title: "Real Estate Tokenization Market Reaches $5B in Assets",
    summary: "Blockchain-based real estate platforms democratize property investment worldwide.",
    read_time: 4,
    date: "2024-12-10",
    body: "Real estate tokenization transforms property investment by enabling fractional ownership through blockchain technology, making commercial real estate accessible to retail investors.\n\n- Market Growth: $5B in tokenized real estate across 15 countries, with projections reaching $16B by 2027.\n- Key Benefits: Fractional ownership from $100, instant liquidity, automated rent distribution, and reduced transaction costs.\n- Leading Platforms: RealT, Harbor, and Elevated Returns pioneer the space with diverse property portfolios.\n- Regulatory Progress: Securities frameworks in Switzerland, Singapore, and US states enable compliant tokenized offerings.",
    image_url: "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=800"
  }
];

const categories = ["All", "Market Analysis", "Technology", "Regulation", "DeFi", "CBDC", "NFT", "Security", "Altcoins", "Enterprise", "Layer 2", "Gaming", "Stablecoins", "Privacy", "Mining", "Tokenization"];

export default function NewsPage() {
  return (
    <div className="min-h-screen bg-darkmode pt-20 pb-16">
      <div className="container mx-auto lg:max-w-screen-xl px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-white text-4xl font-bold mb-4">Latest News</h1>
            <p className="text-muted text-opacity-80 text-lg">
              Stay informed with the latest cryptocurrency news, market analysis, and industry insights
            </p>
          </div>

          {/* Category Filter */}
          <div className="flex flex-wrap justify-center gap-4 mb-12">
            {categories.map((category, index) => (
              <button
                key={index}
                className={`px-6 py-3 rounded-full border transition-all duration-300 ${
                  index === 0
                    ? "bg-primary text-white border-primary"
                    : "bg-transparent text-muted border-dark_border hover:border-primary hover:text-primary"
                }`}
              >
                {category}
              </button>
            ))}
          </div>

          {/* News Grid */}
          <div className="grid lg:grid-cols-2 gap-8 mb-12">
            {newsData.map((article, index) => (
              <article
                key={article.id}
                className={`bg-dark_grey bg-opacity-50 rounded-lg overflow-hidden hover:bg-opacity-70 transition-all duration-300 ${
                  index === 0 ? "lg:col-span-2" : ""
                }`}
              >
                <div className={`${index === 0 ? "lg:flex" : ""}`}>
                  <div className={`${index === 0 ? "lg:w-1/2" : ""}`}>
                    <div className="relative h-48 overflow-hidden">
                      <Image
                        src={article.image_url}
                        alt={article.title}
                        fill
                        className="object-cover"
                      />
                    </div>
                  </div>
                  <div className={`p-6 ${index === 0 ? "lg:w-1/2 lg:flex lg:flex-col lg:justify-center" : ""}`}>
                    <div className="flex items-center gap-4 mb-3">
                      <span className="bg-primary bg-opacity-20 text-primary px-3 py-1 rounded-full text-sm">
                        {article.category}
                      </span>
                      <span className="text-muted text-opacity-60 text-sm">{article.read_time} min read</span>
                    </div>
                    <h2 className={`text-white font-semibold mb-3 hover:text-primary transition-colors cursor-pointer ${
                      index === 0 ? "text-2xl" : "text-xl"
                    }`}>
                      {article.title}
                    </h2>
                    <p className="text-muted text-opacity-80 mb-4">
                      {article.summary}
                    </p>
                    <div className="flex items-center justify-between">
                      <span className="text-muted text-opacity-60 text-sm">
                        {new Date(article.date).toLocaleDateString()}
                      </span>
                      <Link 
                        href={`/news/${article.id}`}
                        className="text-primary hover:text-white transition-colors flex items-center gap-2"
                      >
                        Read More
                        <Icon icon="tabler:arrow-right" width="16" height="16" />
                      </Link>
                    </div>
                  </div>
                </div>
              </article>
            ))}
          </div>

          {/* Newsletter Subscription */}
          <div className="bg-gradient-to-r from-primary to-charcoalGray rounded-lg p-8 text-center">
            <h3 className="text-white text-2xl font-semibold mb-4">Stay Updated</h3>
            <p className="text-muted text-opacity-80 mb-6">
              Subscribe to our newsletter for the latest cryptocurrency news and market insights delivered to your inbox.
            </p>
            <div className="max-w-md mx-auto flex gap-4">
              <input
                type="email"
                placeholder="Enter your email"
                className="flex-1 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-lg px-4 py-3 text-white placeholder-muted"
              />
              <button className="bg-white text-primary px-6 py-3 rounded-lg font-semibold hover:bg-opacity-90 transition-all">
                Subscribe
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
