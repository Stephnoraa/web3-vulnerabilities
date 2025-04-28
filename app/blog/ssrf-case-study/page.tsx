import Link from "next/link";
import Image from "next/image";
import { ArrowLeft, Calendar, Clock, Download, ExternalLink, Share, User } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default function SsrfCaseStudyPage() {
  return (
    <div className="flex min-h-screen flex-col bg-slate-50 dark:bg-slate-900">
      <header className="sticky top-0 z-10 border-b bg-white/80 backdrop-blur-sm dark:bg-slate-950/80">
        <div className="container flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
          <Link href="/blog" className="flex items-center gap-2">
            <ArrowLeft className="h-4 w-4" />
            <span className="text-sm font-medium">Back to Blog</span>
          </Link>
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon">
              <Share className="h-4 w-4" />
              <span className="sr-only">Share</span>
            </Button>
            <Button variant="ghost" size="icon">
              <Download className="h-4 w-4" />
              <span className="sr-only">Download</span>
            </Button>
          </div>
        </div>
      </header>

      <main className="flex-1 py-12">
        <article className="container px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-3xl">
            <h1 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl dark:text-white">
              SSRF Attacks Against NFT Platforms: A Case Study
            </h1>
            <p className="mt-4 text-slate-600 dark:text-slate-400">
              In February 2025, a major NFT marketplace experienced a significant security breach due to a Server-Side
              Request Forgery (SSRF) vulnerability in their metadata fetching service.
            </p>
          </div>
        </article>
      </main>

      <footer className="border-t bg-white py-8 dark:bg-slate-950">
        <div className="container px-4 text-center text-xs text-slate-500 sm:px-6 lg:px-8 dark:text-slate-400">
          <p>© 2025 Web3 Security Research. Educational purposes only.</p>
        </div>
      </footer>
    </div>
  );
}
