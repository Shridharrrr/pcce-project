"use client";

import Link from "next/link";
import { useAuth } from "../contexts/AuthContext";

export default function Home() {
  const { user } = useAuth();

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex min-h-screen w-full max-w-3xl flex-col items-center justify-between py-32 px-16 bg-white dark:bg-black sm:items-start">
        <div className="flex items-center justify-between w-full">
          <h1 className="text-2xl font-bold text-gray-900">Planora</h1>
          {user ? (
            <Link
              href="/dashboard"
              className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg font-medium transition-colors"
            >
              Go to Dashboard
            </Link>
          ) : (
            <Link
              href="/auth"
              className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg font-medium transition-colors"
            >
              Get Started
            </Link>
          )}
        </div>
        
        <div className="flex flex-col items-center gap-6 text-center sm:items-start sm:text-left">
          <h1 className="max-w-xs text-3xl font-semibold leading-10 tracking-tight text-black dark:text-zinc-50">
            Plan Your Child's Future Education
          </h1>
          <p className="max-w-md text-lg leading-8 text-zinc-600 dark:text-zinc-400">
            Planora helps you save and plan for your child's education expenses. 
            Get personalized quotes and track your savings progress with confidence.
          </p>
        </div>
        
        <div className="flex flex-col gap-4 text-base font-medium sm:flex-row">
          <Link
            href="/auth"
            className="flex h-12 w-full items-center justify-center gap-2 rounded-full bg-blue-500 px-5 text-white transition-colors hover:bg-blue-600 md:w-[200px]"
          >
            Start Planning
          </Link>
          <Link
            href="/auth"
            className="flex h-12 w-full items-center justify-center rounded-full border border-solid border-gray-300 px-5 transition-colors hover:border-blue-500 hover:bg-blue-50 md:w-[200px]"
          >
            Learn More
          </Link>
        </div>
      </main>
    </div>
  );
}