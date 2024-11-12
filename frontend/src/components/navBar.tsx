import ThemeSwitcher from "./themeSwitcher";

interface NavBarProps {
  children: React.ReactNode;
}

function NavBar({ children }: NavBarProps) {
  return (
    <div className="navbar backdrop-blur-lg sticky top-0 z-10">
      <div className="navbar-start">
        <a className="btn btn-ghost text-xl">MadMoneyAI</a>
      </div>
      <div className="navbar-end flex gap-4">
        <ThemeSwitcher />
        {children}
      </div>
    </div>
  );
}

export default NavBar;
