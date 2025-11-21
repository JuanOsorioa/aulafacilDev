import { useRoutes } from "react-router-dom";
import "./App.css";

import { Layout } from "./components/Layout.jsx";
import { ProtectedRoute } from "./components/ProtectedRoute.jsx";

// Público
import Login from "./pages/Login.jsx";
import Register from "./pages/Register.jsx";
import Home from "./pages/Home.jsx";

// Estudiante (pantalla principal)
import StudentReservations from "./pages/StudentReservations.jsx";

// Admin
import AdminReservations from "./pages/AdminReservations.jsx";
import AdminAulas from "./pages/AdminAulas.jsx";
import AdminReportes from "./pages/AdminReportes.jsx";

const routes = [
  // Rutas públicas
  { path: "/login", element: <Login /> },
  { path: "/registro", element: <Register /> },
  {
    path: "/",
    element: (
      <Layout>
        <Home />
      </Layout>
    ),
  },

  // Estudiante
  {
    element: (
      <Layout>
        <ProtectedRoute />
      </Layout>
    ),
    children: [
      { path: "/estudiante/reservas", element: <StudentReservations /> },
    ],
  },

  // Admin
  {
    element: (
      <Layout>
        <ProtectedRoute requiredAdmin />
      </Layout>
    ),
    children: [
      { path: "/admin/reservas", element: <AdminReservations /> },
      { path: "/admin/aulas", element: <AdminAulas /> },
      { path: "/admin/reportes", element: <AdminReportes /> },
    ],
  },
];

function App() {
  return useRoutes(routes);
}

export default App;
