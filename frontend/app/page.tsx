import Link from "next/link";

export default function HomePage() {
  return <main className="min-h-screen p-10"><section className="card mx-auto max-w-5xl p-10"><p className="text-sm uppercase tracking-[0.35em] text-violet-300">AI Code Review Mentor</p><h1 className="mt-6 text-6xl font-semibold tracking-tight">Review code. Teach developers. Learn team patterns.</h1><p className="mt-6 max-w-2xl text-lg text-zinc-300">A production-grade portfolio system for GitHub pull request review, mentoring feedback, RAG documentation search, and learning analytics.</p><Link href="/dashboard" className="mt-8 inline-flex rounded-full bg-white px-5 py-3 font-medium text-black">Open dashboard</Link></section></main>;
}
