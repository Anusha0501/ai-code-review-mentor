import Link from "next/link";

const links = ["dashboard", "reviews", "analytics", "learning", "settings"];

export function Nav() {
  return <nav className="flex gap-4 text-sm text-zinc-300">{links.map((link) => <Link key={link} href={`/${link}`} className="hover:text-white">/{link}</Link>)}</nav>;
}
