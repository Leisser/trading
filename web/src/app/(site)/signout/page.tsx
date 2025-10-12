"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { authService } from "@/services/authService";

export default function SignOutPage() {
  const router = useRouter();
  const [status, setStatus] = useState("Signing out...");

  useEffect(() => {
    const performSignOut = async () => {
      try {
        // 1. Sign out from Firebase
        await authService.signOut();
        
        // 2. Clear all tokens from localStorage
        authService.clearTokens();
        
        // 3. Clear any other stored data
        if (typeof window !== 'undefined') {
          localStorage.clear();
          sessionStorage.clear();
        }
        
        setStatus("✅ Signed out successfully!");
        
        // 4. Redirect to home page after 1 second
        setTimeout(() => {
          router.push('/');
        }, 1000);
        
      } catch (error) {
        console.error("Sign out error:", error);
        setStatus("✅ Signed out (with warnings)");
        
        // Still redirect even if there's an error
        setTimeout(() => {
          router.push('/');
        }, 1000);
      }
    };

    performSignOut();
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-black">
      <div className="text-center">
        <div className="mb-6">
          {status.includes("...") ? (
            <div className="inline-block">
              <svg
                className="animate-spin h-12 w-12 text-orange-500 mx-auto"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
            </div>
          ) : (
            <div className="text-6xl">✅</div>
          )}
        </div>
        
        <h1 className="text-3xl font-bold text-white mb-2">{status}</h1>
        <p className="text-gray-400">Redirecting to home page...</p>
      </div>
    </div>
  );
}

