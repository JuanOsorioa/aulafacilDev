import PublicHeader from "./PublicHeader.jsx";
import PrivateHeader from "./PrivateHeader.jsx";
import { useAuth } from "../context/AuthContext.jsx";

export function Layout({ children }) {
  const { user } = useAuth();

  return (
    <div className="layout">
      {user ? <PrivateHeader /> : <PublicHeader />}

      <main className="page">
        {children}
      </main>
    </div>
  );
}
