import { HeaderItem } from "@/types/menu";

export const headerData: HeaderItem[] = [
  { label: "Trading", href: "/trading/spot" },
  { label: "Wallet", href: "/wallet" },
  { label: "Board", href: "/board" },
  { 
    label: "Index", 
    href: "/index",
    submenu: [
      { label: "Advanced Orders", href: "/index/advanced-orders" },
      { label: "Automated Strategies", href: "/index/automated-strategies" },
      { label: "Leverage Trading", href: "/index/leverage-trading" }
    ]
  },
  { label: "Portfolio", href: "/#portfolio" },
  { label: "Buy & Sell", href: "/#main-banner" },
  { label: "Development", href: "/#development" },
  { label: "Work", href: "/#work" },
  { label: "Upgrade", href: "/#upgrade" },
];
