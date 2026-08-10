import Link from "next/link";

export default function Navbar(){

    return (
    <nav className="p-4 border-b flex gap-6">
      <Link href="/">Home</Link>

      <Link href="/login">
        Login
      </Link>

      <Link href="/signup">
        Signup
      </Link>

      <Link href="/dashboard">
        Dashboard
      </Link>
    </nav>
    )
}