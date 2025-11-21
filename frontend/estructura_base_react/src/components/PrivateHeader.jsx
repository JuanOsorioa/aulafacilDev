import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import logo from "../assets/images/logo.png";
import "../assets/styles/PrivateHeader.css";

export default function PrivateHeader() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/"); // vuelve al home público
  };

  return (
    <header className="private-header">
      <div className="ph-inner">

        <div className="ph-logo-box">
          <img src={logo} alt="Logo AulaFácil" className="ph-logo" />
        </div>

        <span className="ph-title">AulaFácil</span>

        <button className="ph-logout" onClick={handleLogout}>
          Cerrar sesión
        </button>

      </div>
    </header>
  );
}
