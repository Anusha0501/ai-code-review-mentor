import { Nav } from "../../components/ui/nav";

export default function DashboardPage() {
  return <main className="min-h-screen p-8"><Nav /><section className="card mt-8 p-8"><h1 className="text-4xl font-semibold">Team Review Dashboard</h1><p className="mt-3 text-zinc-300">Track review volume, recurring mistakes, learning progress, and open pull request risk.</p><div className="mt-8 grid gap-4 md:grid-cols-3">{["Reviews", "Findings", "Learning Wins"].map((label, index) => <div className="rounded-2xl border border-white/10 p-5" key={label}><p className="text-zinc-400">{label}</p><p className="mt-3 text-4xl font-semibold">{[24, 87, 13][index]}</p></div>)}</div></section></main>;
}
