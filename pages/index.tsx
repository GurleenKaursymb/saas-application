"use client"

import { useAuth, SignedIn, SignedOut, SignInButton, UserButton } from '@clerk/nextjs';
import { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkBreaks from 'remark-breaks';
import { fetchEventSource } from '@microsoft/fetch-event-source';

export default function Product() {
  const { getToken } = useAuth();
  const [idea, setIdea] = useState<string>('...loading');

  useEffect(() => {
    let buffer = '';
    (async () => {
      const jwt = await getToken();
      if (!jwt) {
        setIdea('Authentication required');
        return;
      }

      await fetchEventSource('/api', {
        headers: { Authorization: `Bearer ${jwt}` },
        onmessage(ev) {
            // Unescape the literal '\\n' back to real line breaks
            const chunk = ev.data.replace(/\\n/g, "\n");
            buffer += chunk;
            setIdea(buffer);
        },
        onerror(err) {
          console.error('SSE error:', err);
        }
      });
    })();
  }, []);

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 py-12 px-4 flex flex-col items-center">
      <div className="w-full max-w-4xl">
        
        {/* Header */}
        <header className="text-center mb-10">
          <h1 className="text-5xl font-extrabold bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent mb-3">
            Business Idea Generator
          </h1>
          <p className="text-slate-400 text-lg font-medium">
            AI-powered innovation at your fingertips
          </p>
        </header>

        {/* Main Content Card */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-8 backdrop-blur-sm">
          
          <SignedOut>
            <div className="text-center py-10">
              <p className="text-slate-300 text-lg mb-6">
                Please sign in to generate AI business ideas.
              </p>
              <SignInButton mode="modal">
                <button className="px-6 py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-xl transition shadow-lg shadow-indigo-500/20">
                  Sign In / Sign Up
                </button>
              </SignInButton>
            </div>
          </SignedOut>

          <SignedIn>
            <div className="flex justify-between items-center pb-6 mb-6 border-b border-slate-800">
              <span className="text-xs font-semibold uppercase tracking-wider text-indigo-400 bg-indigo-950/80 border border-indigo-800 px-3 py-1 rounded-full">
                AI Output
              </span>
              <UserButton />
            </div>

            {idea === '...loading' ? (
              <div className="flex flex-col items-center justify-center py-16 space-y-4">
                <div className="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
                <p className="text-slate-400 animate-pulse font-medium">Generating your business idea...</p>
              </div>
            ) : (
                <div className="prose prose-invert max-w-none space-y-4 leading-relaxed text-slate-200 [&_h1]:text-2xl [&_h1]:font-bold [&_h1]:text-indigo-400 [&_h1]:mt-6 [&_h1]:mb-3 [&_h2]:text-xl [&_h2]:font-semibold [&_h2]:text-blue-400 [&_h2]:mt-5 [&_h2]:mb-2 [&_h3]:text-lg [&_h3]:font-medium [&_h3]:text-slate-100 [&_p]:mb-3 [&_ul]:list-disc [&_ul]:pl-5 [&_ul]:space-y-1 [&_li]:text-slate-300 [&_strong]:text-indigo-300 [&_strong]:font-semibold">
                <ReactMarkdown remarkPlugins={[remarkGfm, remarkBreaks]}>
                  {idea}
                </ReactMarkdown>
              </div>
            )}
          </SignedIn>

        </div>
      </div>
    </main>
  );
}