"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";
import Logo from "@/components/Layout/Header/Logo";
import { useState } from "react";
import Loader from "@/components/Common/Loader";
import { Icon } from "@iconify/react";
import { authService, UserRegistrationData } from "@/services/authService";

interface SignUpProps {
  onSuccess?: () => void;
}

const SignUp = ({ onSuccess }: SignUpProps = {}) => {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [currentStep, setCurrentStep] = useState(1);

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [idImages, setIdImages] = useState({
    idFront: null as File | null,
    idBack: null as File | null,
    passport: null as File | null,
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>, type: 'idFront' | 'idBack' | 'passport') => {
    const file = e.target.files?.[0];
    if (file) {
      // Validate file type
      if (!file.type.startsWith('image/')) {
        setError('Please upload only image files');
        return;
      }
      
      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        setError('File size must be less than 5MB');
        return;
      }

      setIdImages(prev => ({
        ...prev,
        [type]: file
      }));
      setError("");
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    // Validation
    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (formData.password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    // Check if at least one ID image is provided
    if (!idImages.idFront && !idImages.passport) {
      setError("Please upload at least one ID document (ID card front or passport)");
      return;
    }

    setLoading(true);

    try {
      // Step 1: Create Firebase user
      const userCredential = await authService.registerWithEmail({
        name: formData.name,
        email: formData.email,
        password: formData.password,
        idFrontImage: idImages.idFront || undefined,
        idBackImage: idImages.idBack || undefined,
        passportImage: idImages.passport || undefined,
      });

      // Step 2: Sync with backend (auto-creates user if doesn't exist)
      await authService.syncFirebaseUser(userCredential.user);

      // Step 3: Success - user is now registered and logged in!
      setSuccess("Registration successful! Redirecting...");
      
      // Close the modal if callback provided
      if (onSuccess) {
        onSuccess();
      }
      
      // Redirect to portfolio after short delay
      setTimeout(() => {
        window.location.href = '/#portfolio';
      }, 1500);

    } catch (error: any) {
      setError(error.message || "Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleSignUp = async () => {
    setError("");
    setLoading(true);

    try {
      const userCredential = await authService.signInWithGoogle();
      
      // Sync with backend (auto-creates user if doesn't exist)
      await authService.syncFirebaseUser(userCredential.user);

      // Success - user is now registered and logged in!
      setSuccess("Registration successful! Redirecting...");
      
      // Close the modal if callback provided
      if (onSuccess) {
        onSuccess();
      }
      
      setTimeout(() => {
        window.location.href = '/#portfolio';
      }, 1500);

    } catch (error: any) {
      setError(error.message || "Google signup failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleGithubSignUp = async () => {
    setError("");
    setLoading(true);

    try {
      const userCredential = await authService.signInWithGithub();
      
      // Sync with backend (auto-creates user if doesn't exist)
      await authService.syncFirebaseUser(userCredential.user);

      // Success - user is now registered and logged in!
      setSuccess("Registration successful! Redirecting...");
      
      // Close the modal if callback provided
      if (onSuccess) {
        onSuccess();
      }
      
      setTimeout(() => {
        window.location.href = '/#portfolio';
      }, 1500);

    } catch (error: any) {
      setError(error.message || "GitHub signup failed. Please try again.");
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

      {success && (
        <div className="bg-green-900 bg-opacity-20 border border-green-500 rounded-lg p-4 mb-6">
          <div className="flex items-center">
            <Icon icon="tabler:check-circle" width="20" height="20" className="text-green-400 mr-2" />
            <span className="text-green-300 text-sm">{success}</span>
          </div>
        </div>
      )}

      {/* OAuth Sign Up */}
      <div className="grid grid-cols-2 gap-3 mb-6">
        <button
          type="button"
          onClick={handleGoogleSignUp}
          disabled={loading}
          className="w-full inline-flex justify-center py-2 px-4 border border-dark_border rounded-md shadow-sm bg-dark_grey text-sm font-medium text-white hover:bg-dark_grey/80 transition-colors disabled:opacity-50"
        >
          <Icon icon="logos:google-icon" width="20" height="20" />
          <span className="ml-2">Google</span>
        </button>

        <button
          type="button"
          onClick={handleGithubSignUp}
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

      <form onSubmit={handleSubmit}>
        {/* Step 1: Basic Information */}
        {currentStep === 1 && (
          <>
            <div className="mb-[22px]">
              <input
                type="text"
                placeholder="Full Name"
                name="name"
                required
                value={formData.name}
                onChange={handleInputChange}
                className="w-full rounded-md border border-dark_border border-opacity-60 border-solid bg-transparent px-5 py-3 text-base text-dark outline-none transition placeholder:text-grey focus:border-primary focus-visible:shadow-none text-white dark:focus:border-primary"
              />
            </div>
            <div className="mb-[22px]">
              <input
                type="email"
                placeholder="Email"
                name="email"
                required
                value={formData.email}
                onChange={handleInputChange}
                className="w-full rounded-md border border-dark_border border-opacity-60 border-solid bg-transparent px-5 py-3 text-base text-dark outline-none transition placeholder:text-grey focus:border-primary focus-visible:shadow-none text-white dark:focus:border-primary"
              />
            </div>
            <div className="mb-[22px]">
              <input
                type="password"
                placeholder="Password (min 6 characters)"
                name="password"
                required
                value={formData.password}
                onChange={handleInputChange}
                className="w-full rounded-md border border-dark_border border-opacity-60 border-solid bg-transparent px-5 py-3 text-base text-dark outline-none transition placeholder:text-grey focus:border-primary focus-visible:shadow-none text-white dark:focus:border-primary"
              />
            </div>
            <div className="mb-[22px]">
              <input
                type="password"
                placeholder="Confirm Password"
                name="confirmPassword"
                required
                value={formData.confirmPassword}
                onChange={handleInputChange}
                className="w-full rounded-md border border-dark_border border-opacity-60 border-solid bg-transparent px-5 py-3 text-base text-dark outline-none transition placeholder:text-grey focus:border-primary focus-visible:shadow-none text-white dark:focus:border-primary"
              />
            </div>
            <div className="mb-9">
              <button
                type="button"
                onClick={() => setCurrentStep(2)}
                className="flex w-full items-center text-18 font-medium justify-center rounded-md bg-primary px-5 py-3 text-darkmode transition duration-300 ease-in-out hover:bg-transparent hover:text-primary border-primary border"
              >
                Next: ID Verification
              </button>
            </div>
          </>
        )}

        {/* Step 2: ID Verification */}
        {currentStep === 2 && (
          <div className="max-h-96 overflow-y-auto pr-2">
            <div className="text-center mb-6">
              <Icon icon="tabler:id" width="48" height="48" className="text-primary mx-auto mb-2" />
              <h3 className="text-lg font-semibold text-white">ID Verification Required</h3>
              <p className="text-sm text-muted">Please upload clear photos of your ID documents</p>
            </div>

            {/* Important Disclaimer */}
            <div className="bg-yellow-900 bg-opacity-20 border border-yellow-500 rounded-lg p-4 mb-6 max-h-32 overflow-y-auto">
              <div className="flex items-start">
                <Icon icon="tabler:alert-triangle" width="20" height="20" className="text-yellow-400 mr-3 mt-0.5 flex-shrink-0" />
                <div className="flex-1">
                  <h4 className="text-yellow-300 text-sm font-semibold mb-2">Important Notice</h4>
                  <div className="text-yellow-200 text-xs leading-relaxed space-y-2">
                    <p>
                      <strong>Account Deactivation Warning:</strong> Only upload valid government-issued ID cards or passports. 
                      Any other documents (driver's license, student ID, work ID, etc.) will result in immediate account deactivation 
                      without notice.
                    </p>
                    <p>
                      <strong>Document Requirements:</strong> Ensure your documents are clear, unexpired, and government-issued. 
                      Blurry, expired, or non-government documents will be rejected and may result in account suspension.
                    </p>
                    <p>
                      <strong>Verification Process:</strong> All uploaded documents undergo automated and manual verification. 
                      False or fraudulent documents will result in permanent account termination.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div className="mb-[22px]">
              <label className="block text-sm font-medium text-white mb-2">
                ID Card Front (Required)
              </label>
              <input
                type="file"
                accept="image/*"
                onChange={(e) => handleFileChange(e, 'idFront')}
                className="w-full rounded-md border border-dark_border border-opacity-60 border-solid bg-transparent px-5 py-3 text-base text-white outline-none transition focus:border-primary focus-visible:shadow-none"
              />
              {idImages.idFront && (
                <p className="text-green-400 text-xs mt-1">✓ {idImages.idFront.name}</p>
              )}
            </div>

            <div className="mb-[22px]">
              <label className="block text-sm font-medium text-white mb-2">
                ID Card Back (Optional)
              </label>
              <input
                type="file"
                accept="image/*"
                onChange={(e) => handleFileChange(e, 'idBack')}
                className="w-full rounded-md border border-dark_border border-opacity-60 border-solid bg-transparent px-5 py-3 text-base text-white outline-none transition focus:border-primary focus-visible:shadow-none"
              />
              {idImages.idBack && (
                <p className="text-green-400 text-xs mt-1">✓ {idImages.idBack.name}</p>
              )}
            </div>

            <div className="mb-[22px]">
              <label className="block text-sm font-medium text-white mb-2">
                Passport (Alternative to ID)
              </label>
              <input
                type="file"
                accept="image/*"
                onChange={(e) => handleFileChange(e, 'passport')}
                className="w-full rounded-md border border-dark_border border-opacity-60 border-solid bg-transparent px-5 py-3 text-base text-white outline-none transition focus:border-primary focus-visible:shadow-none"
              />
              {idImages.passport && (
                <p className="text-green-400 text-xs mt-1">✓ {idImages.passport.name}</p>
              )}
            </div>

            {/* Disclaimer Agreement Checkbox */}
            <div className="mb-6">
              <label className="flex items-start space-x-3 cursor-pointer">
                <input
                  type="checkbox"
                  required
                  className="mt-1 w-4 h-4 text-primary bg-transparent border border-dark_border rounded focus:ring-primary focus:ring-2 flex-shrink-0"
                />
                <div className="flex-1 max-h-20 overflow-y-auto">
                  <span className="text-yellow-200 text-xs leading-relaxed block">
                    I understand that only government-issued ID cards or passports are acceptable. 
                    I acknowledge that uploading any other type of document will result in immediate 
                    account deactivation without notice. I confirm that the documents I will upload 
                    are valid, government-issued, and belong to me. I agree to the verification process 
                    and understand that false documents will result in permanent account termination.
                  </span>
                </div>
              </label>
            </div>

            <div className="flex space-x-3 mb-9">
              <button
                type="button"
                onClick={() => setCurrentStep(1)}
                className="flex-1 py-3 px-4 border border-dark_border text-sm font-medium rounded-md text-white bg-dark_grey hover:bg-dark_grey/80 transition-colors"
              >
                Back
              </button>
              <button
                type="submit"
                disabled={loading}
                className="flex-1 flex items-center text-18 font-medium justify-center rounded-md bg-primary px-5 py-3 text-darkmode transition duration-300 ease-in-out hover:bg-transparent hover:text-primary border-primary border disabled:opacity-50"
              >
                {loading ? "Creating Account..." : "Create Account"} {loading && <Loader />}
              </button>
            </div>
          </div>
        )}
      </form>

      <p className="text-body-secondary mb-4 text-white text-base">
        By creating an account you are agree with our{" "}
        <Link href="/privacy" className="text-primary hover:underline">
          Privacy
        </Link>{" "}
        and{" "}
        <Link href="/terms" className="text-primary hover:underline">
          Terms
        </Link>
      </p>

      <p className="text-body-secondary text-white text-base">
        Already have an account?
        <Link href="/signin" className="pl-2 text-primary hover:underline">
          Sign In
        </Link>
      </p>
    </>
  );
};

export default SignUp;
