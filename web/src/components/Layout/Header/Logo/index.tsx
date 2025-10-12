import { getImagePrefix } from "@/utils/utils";
import Image from "next/image";
import Link from "next/link";

const Logo: React.FC = () => {
  return (
    <Link href="/" className="group">
      <div className="flex items-center gap-3">
        <div className="relative">
          <Image
            src={`${getImagePrefix()}images/logo/logo.svg`}
            alt="Fluxor Logo"
            width={160}
            height={50}
            style={{ width: "auto", height: "auto" }}
            quality={100}
            className="transition-all duration-300 group-hover:scale-105 group-hover:brightness-110"
            priority
          />
          <div className="absolute inset-0 bg-gradient-to-r from-primary/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-lg"></div>
        </div>
      </div>
    </Link>
  );
};

export default Logo;
