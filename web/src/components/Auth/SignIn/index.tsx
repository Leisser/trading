"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import toast from "react-hot-toast";
import Logo from "@/components/Layout/Header/Logo";
import Loader from "@/components/Common/Loader";
import { Icon } from "@iconify/react";
import { authService } from "@/services/authService";

const Signin = () => {
  const router = useRouter();

  const [loginData, setLoginData] = useState({
    email: "",
    password: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setLoginData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const loginUser = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      // Step 1: Sign in with Firebase
      const userCredential = await authService.signInWithEmail(loginData.email, loginData.password);
      
      // Step 2: Get Firebase ID token
      const idToken = await userCredential.user.getIdToken();
      
      // Step 3: Convert Firebase token to backend tokens
      const tokens = await authService.convertToken(idToken);
      
      // Step 4: Store tokens
      authService.setTokens(tokens);
      
      // Step 5: Success
      toast.success("Login successful");
      router.push("/dashboard");
      
    } catch (error: any) {
      setError(error.message || "Login failed. Please try again.");
      toast.error(error.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleSignIn = async () => {
    setError("");
    setLoading(true);

    try {
      const userCredential = await authService.signInWithGoogle();
      const idToken = await userCredential.user.getIdToken();
      const tokens = await authService.convertToken(idToken);
      authService.setTokens(tokens);
      
      toast.success("Login successful");
      router.push("/dashboard");
      
    } catch (error: any) {
      setError(error.message || "Google sign-in failed");
      toast.error(error.message || "Google sign-in failed");
    } finally {
      setLoading(false);
    }
  };

  const handleGithubSignIn = async () => {
    setError("");
    setLoading(true);

    try {
      const userCredential = await authService.signInWithGithub();
      const idToken = await userCredential.user.getIdToken();
      const tokens = await authService.convertToken(idToken);
      authService.setTokens(tokens);
      
      toast.success("Login successful");
      router.push("/dashboard");
      
    } catch (error: any) {
      setError(error.message || "GitHub sign-in failed");
      toast.error(error.message || "GitHub sign-in failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="mb-10 text-center mx-auto inline-block max-w-[160px]">
        <Logo />
      </div>

      {error && (
        <div className="bg-red-900 bg-opacity-20 border border-red-500 rounded-lg p-4 mb-6">
          <div className="flex items-center">
            <Icon icon="tabler:alert-circle" width="20" height="20" className="text-red-400 mr-2" />
            <span className="text-red-300 text-sm">{error}</span>
          </div>
        </div>
      )}

      {/* OAuth Sign In */}
      <div className="grid grid-cols-2 gap-3 mb-6">
        <button
          type="button"
          onClick={handleGoogleSignIn}
          disabled={loading}
          className="w-full inline-flex justify-center py-2 px-4 border border-dark_border rounded-md shadow-sm bg-dark_grey text-sm font-medium text-white hover:bg-dark_grey/80 transition-colors disabled:opacity-50"
        >
          <Icon icon="logos:google-icon" width="20" height="20" />
          <span className="ml-2">Google</span>
        </button>

        <button
          type="button"
          onClick={handleGithubSignIn}
          disabled={loading}
          className="w-full inline-flex justify-center py-2 px-4 border border-dark_border rounded-md shadow-sm bg-dark_grey text-sm font-medium text-white hover:bg-dark_grey/80 transition-colors disabled:opacity-50"
        >
          <Icon icon="logos:github-icon" width="20" height="20" />
          <span className="ml-2">GitHub</span>
        </button>
      </div>

      <span className="z-1 relative my-8 block text-center before:content-[''] before:absolute before:h-px before:w-40% before:bg-dark_border before:bg-opacity-60 before:left-0 before:top-3 after:content-[''] after:absolute after:h-px after:w-40% after:bg-dark_border after:bg-opacity-60 after:top-3 after:right-0">
        <span className="text-body-secondary relative z-10 inline-block px-3 text-base text-white">
          OR
        </span>
      </span>

      <form onSubmit={loginUser}>
        <div className="mb-[22px]">
          <input
            type="email"
            name="email"
            placeholder="Email"
            required
            value={loginData.email}
            onChange={handleInputChange}
            className="w-full rounded-md border border-dark_border border-opacity-60 border-solid bg-transparent px-5 py-3 text-base text-dark outline-none transition placeholder:text-grey focus:border-primary focus-visible:shadow-none text-white dark:focus:border-primary"
          />
        </div>
        <div className="mb-[22px]">
          <input
            type="password"
            name="password"
            placeholder="Password"
            required
            value={loginData.password}
            onChange={handleInputChange}
            className="w-full rounded-md border border-dark_border border-opacity-60 border-solid bg-transparent px-5 py-3 text-base text-dark outline-none transition placeholder:text-grey focus:border-primary focus-visible:shadow-none text-white dark:focus:border-primary"
          />
        </div>
        <div className="mb-9">
          <button
            type="submit"
            disabled={loading}
            className="bg-primary w-full py-3 rounded-lg text-18 font-medium border border-primary hover:text-primary hover:bg-transparent disabled:opacity-50 flex items-center justify-center"
          >
            Sign In {loading && <Loader />}
          </button>
        </div>
      </form>

      <Link
        href="/forgot-password"
        className="mb-2 inline-block text-base text-dark hover:text-primary text-white dark:hover:text-primary"
      >
        Forgot Password?
      </Link>
      <p className="text-body-secondary text-white text-base">
        Not a member yet?{" "}
        <Link href="/signup" className="text-primary hover:underline">
          Sign Up
        </Link>
      </p>
    </>
  );
};

export default Signin;