/** @type {import('next').NextConfig} */
const isProd = process.env.NODE_ENV === "production";

const nextConfig = {
  basePath: "",
  assetPrefix: "",
  output: "standalone",
  images: {
    unoptimized: true,
  },
};

export default nextConfig;

 