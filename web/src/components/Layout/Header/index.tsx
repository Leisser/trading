"use client";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { headerData } from "../Header/Navigation/menuData";
import Logo from "./Logo";
import Image from "next/image";
import HeaderLink from "../Header/Navigation/HeaderLink";
import MobileHeaderLink from "../Header/Navigation/MobileHeaderLink";
import Signin from "@/components/Auth/SignIn";
import SignUp from "@/components/Auth/SignUp";
import { useTheme } from "next-themes";
import { authService } from "@/services/authService";
import { Icon } from "@iconify/react/dist/iconify.js";

const Header: React.FC = () => {
  const pathUrl = usePathname();
  const router = useRouter();
  const { theme, setTheme } = useTheme();

  const [navbarOpen, setNavbarOpen] = useState(false);
  const [sticky, setSticky] = useState(false);
  const [isSignInOpen, setIsSignInOpen] = useState(false);
  const [isSignUpOpen, setIsSignUpOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isSuperuser, setIsSuperuser] = useState(false);

  const navbarRef = useRef<HTMLDivElement>(null);
  const signInRef = useRef<HTMLDivElement>(null);
  const signUpRef = useRef<HTMLDivElement>(null);
  const mobileMenuRef = useRef<HTMLDivElement>(null);

  const handleScroll = () => {
    setSticky(window.scrollY >= 80);
  };

  const handleClickOutside = (event: MouseEvent) => {
    if (
      signInRef.current &&
      !signInRef.current.contains(event.target as Node)
    ) {
      setIsSignInOpen(false);
    }
    if (
      signUpRef.current &&
      !signUpRef.current.contains(event.target as Node)
    ) {
      setIsSignUpOpen(false);
    }
    if (
      mobileMenuRef.current &&
      !mobileMenuRef.current.contains(event.target as Node) &&
      navbarOpen
    ) {
      setNavbarOpen(false);
    }
  };

  // Check authentication status and superuser
  useEffect(() => {
    const checkAuth = async () => {
      const accessToken = authService.getAccessToken();
      setIsAuthenticated(!!accessToken);

      // Check if user is superuser
      if (accessToken) {
        try {
          const response = await fetch('http://localhost:8000/api/profile/', {
            headers: {
              'Authorization': `Bearer ${accessToken}`,
            },
          });
          if (response.ok) {
            const profile = await response.json();
            setIsSuperuser(profile.is_superuser || false);
          } else {
            setIsSuperuser(false);
          }
        } catch (error) {
          setIsSuperuser(false);
        }
      } else {
        setIsSuperuser(false);
      }
    };
    
    checkAuth();
    const interval = setInterval(checkAuth, 2000); // Check every 2 seconds
    
    // Listen for auth changes (custom event)
    const handleAuthChange = () => {
      checkAuth();
    };
    window.addEventListener('authChanged', handleAuthChange);
    
    return () => {
      clearInterval(interval);
      window.removeEventListener('authChanged', handleAuthChange);
    };
  }, [pathUrl]); // Re-check when path changes

  useEffect(() => {
    window.addEventListener("scroll", handleScroll);
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      window.removeEventListener("scroll", handleScroll);
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [navbarOpen, isSignInOpen, isSignUpOpen]);

  const handleSignOut = async () => {
    try {
      await authService.signOut();
      authService.clearTokens();
      setIsAuthenticated(false);
      setIsSuperuser(false);
      router.push('/');
    } catch (error) {
      console.error('Sign out error:', error);
      authService.clearTokens();
      setIsAuthenticated(false);
      setIsSuperuser(false);
      router.push('/');
    }
  };

  useEffect(() => {
    if (isSignInOpen || isSignUpOpen || navbarOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
  }, [isSignInOpen, isSignUpOpen, navbarOpen]);

  return (
    <header
      className={`fixed top-0 z-40 w-full pb-5 transition-all duration-300 ${
        sticky ? " shadow-lg bg-darkmode pt-5" : "shadow-none md:pt-14 pt-5"
      }`}
    >
      <div className="lg:py-0 py-2">
        <div className="container mx-auto lg:max-w-screen-xl md:max-w-screen-md flex items-center justify-between px-4">
          <Logo />
          <nav className="hidden lg:flex flex-grow items-center gap-8 justify-center">
            {headerData
              .filter(item => {
                // Show Trading, Wallet, and Index only when authenticated
                const authOnlyItems = ['Trading', 'Wallet', 'Index'];
                if (authOnlyItems.includes(item.label)) {
                  return isAuthenticated;
                }
                // Show Board only for superusers
                if (item.label === 'Board') {
                  return isAuthenticated && isSuperuser;
                }
                return true; // Show all other items always
              })
              .map((item, index) => (
                <HeaderLink key={index} item={item} />
              ))}
          </nav>
          <div className="flex items-center gap-4">
            {/* Show Sign Out if authenticated, otherwise Sign In/Sign Up */}
            {isAuthenticated ? (
              <button
                onClick={handleSignOut}
                className="hidden lg:block bg-red-600 text-white border border-red-600 hover:bg-transparent hover:text-red-600 px-4 py-2 rounded-lg transition-colors"
              >
                Sign Out
              </button>
            ) : (
              <Link
                href="#"
                className="hidden lg:block bg-transparent text-primary border hover:bg-primary border-primary hover:text-darkmode px-4 py-2 rounded-lg"
                onClick={() => {
                  setIsSignInOpen(true);
                }}
              >
                Sign In
              </Link>
            )}
            {isSignInOpen && (
              <div className="fixed top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center z-50">
                <div
                  ref={signInRef}
                  className="relative mx-auto w-full max-w-md overflow-hidden rounded-lg px-8 pt-14 pb-8 text-center bg-dark_grey bg-opacity-90 backdrop-blur-md"
                >
                  <button
                    onClick={() => setIsSignInOpen(false)}
                    className="absolute top-0 right-0 mr-8 mt-8 dark:invert"
                    aria-label="Close Sign In Modal"
                  >
                    <Icon
                      icon="tabler:currency-xrp"
                      className="text-white hover:text-primary text-24 inline-block me-2"
                    />
                  </button>
                  <Signin onSuccess={() => setIsSignInOpen(false)} />
                </div>
              </div>
            )}
            {!isAuthenticated && (
              <Link
                href="#"
                className="hidden lg:block bg-primary text-darkmode hover:bg-transparent hover:text-primary border border-primary px-4 py-2 rounded-lg"
                onClick={() => {
                  setIsSignUpOpen(true);
                }}
              >
                Sign Up
              </Link>
            )}
            {isSignUpOpen && (
              <div className="fixed top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center z-50">
                <div
                  ref={signUpRef}
                  className="relative mx-auto w-full max-w-md overflow-hidden rounded-lg bg-dark_grey bg-opacity-90 backdrop-blur-md px-8 pt-14 pb-8 text-center"
                >
                  <button
                    onClick={() => setIsSignUpOpen(false)}
                    className="absolute top-0 right-0 mr-8 mt-8 dark:invert"
                    aria-label="Close Sign Up Modal"
                  >
                    <Icon
                      icon="tabler:currency-xrp"
                      className="text-white hover:text-primary text-24 inline-block me-2"
                    />
                  </button>
                  <SignUp onSuccess={() => setIsSignUpOpen(false)} />
                </div>
              </div>
            )}
            <button
              onClick={() => setNavbarOpen(!navbarOpen)}
              className="block lg:hidden p-2 rounded-lg"
              aria-label="Toggle mobile menu"
            >
              <span className="block w-6 h-0.5 bg-white"></span>
              <span className="block w-6 h-0.5 bg-white mt-1.5"></span>
              <span className="block w-6 h-0.5 bg-white mt-1.5"></span>
            </button>
          </div>
        </div>
        {navbarOpen && (
          <div className="fixed top-0 left-0 w-full h-full bg-black bg-opacity-50 z-40" />
        )}
        <div
          ref={mobileMenuRef}
          className={`lg:hidden fixed top-0 right-0 h-full w-full bg-darkmode shadow-lg transform transition-transform duration-300 max-w-xs ${
            navbarOpen ? "translate-x-0" : "translate-x-full"
          } z-50`}
        >
          <div className="flex items-center justify-between p-4">
            <h2 className="text-lg font-bold text-midnight_text dark:text-midnight_text">
              <Logo />
            </h2>

            {/*  */}
            <button
              onClick={() => setNavbarOpen(false)}
              className="bg-[url('/images/closed.svg')] bg-no-repeat bg-contain w-5 h-5 absolute top-0 right-0 mr-8 mt-8 dark:invert"
              aria-label="Close menu Modal"
            ></button>
          </div>
          <nav className="flex flex-col items-start p-4">
            {headerData
              .filter(item => {
                // Show Trading, Wallet, and Index only when authenticated
                const authOnlyItems = ['Trading', 'Wallet', 'Index'];
                if (authOnlyItems.includes(item.label)) {
                  return isAuthenticated;
                }
                // Show Board only for superusers
                if (item.label === 'Board') {
                  return isAuthenticated && isSuperuser;
                }
                return true; // Show all other items always
              })
              .map((item, index) => (
                <MobileHeaderLink key={index} item={item} />
              ))}
            <div className="mt-4 flex flex-col space-y-4 w-full">
              {isAuthenticated ? (
                <button
                  onClick={() => {
                    handleSignOut();
                    setNavbarOpen(false);
                  }}
                  className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
                >
                  Sign Out
                </button>
              ) : (
                <>
                  <Link
                    href="#"
                    className="bg-transparent border border-primary text-primary px-4 py-2 rounded-lg hover:bg-blue-600 hover:text-white"
                    onClick={() => {
                      setIsSignInOpen(true);
                      setNavbarOpen(false);
                    }}
                  >
                    Sign In
                  </Link>
                  <Link
                    href="#"
                    className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-blue-700"
                    onClick={() => {
                      setIsSignUpOpen(true);
                      setNavbarOpen(false);
                    }}
                  >
                    Sign Up
                  </Link>
                </>
              )}
            </div>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
