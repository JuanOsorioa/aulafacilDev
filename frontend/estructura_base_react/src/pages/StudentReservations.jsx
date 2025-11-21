import { useEffect, useState } from "react";
import {
  cancelReserva,
  createReserva,
  getAulas,
  getReservas,
  getNotificaciones,
  updateReserva,
} from "../api/client";
import { useAuth } from "../context/AuthContext.jsx";
import "../assets/styles/StudentReservations.css";

function formatISO(value) {
  if (!value) return "";
  return new Date(value).toISOString().slice(0, 16);
}

export default function StudentReservations() {
  const { user } = useAuth();

  const [disponibles, setDisponibles] = useState([]);
  const [reservas, setReservas] = useState([]);
  const [filters, setFilters] = useState({ inicio: "", fin: "" });
  const [form, setForm] = useState({ inicio: "", fin: "", id_aula: "" });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [notis, setNotis] = useState([]);
  const [loadingDisponibles, setLoadingDisponibles] = useState(false);
  const [loadingReserva, setLoadingReserva] = useState(false);

  useEffect(() => {
    if (!user) return;
    cargarReservas();
    cargarNotis();
  }, [user]);

  const cargarReservas = async () => {
    setLoading(true);
    try {
      const data = await getReservas();
      setReservas(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const buscarDisponibles = async (e) => {
    e.preventDefault();
    setError("");
    if (!filters.inicio || !filters.fin) {
      setError("Selecciona inicio y fin");
      return;
    }
    if (new Date(filters.inicio) >= new Date(filters.fin)) {
      setError("La hora fin debe ser posterior a inicio");
      return;
    }

    setLoadingDisponibles(true);

    try {
      const data = await getAulas({
        inicio: new Date(filters.inicio).toISOString(),
        fin: new Date(filters.fin).toISOString(),
      });
      setDisponibles(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingDisponibles(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");
    if (!form.inicio || !form.fin || !form.id_aula) {
      setError("Completa inicio, fin y aula");
      return;
    }

    if (new Date(form.inicio) >= new Date(form.fin)) {
      setError("La hora fin debe ser posterior a inicio");
      return;
    }

    setLoadingReserva(true);

    try {
      await createReserva({
        inicio: new Date(form.inicio).toISOString(),
        fin: new Date(form.fin).toISOString(),
        id_aula: form.id_aula,
      });

      setMessage("Reserva creada con éxito");
      setForm({ inicio: "", fin: "", id_aula: "" });
      cargarReservas();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingReserva(false);
    }
  };

  const handleCancel = async (id) => {
    setError("");
    try {
      await cancelReserva(id);
      setMessage("Reserva cancelada");
      cargarReservas();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleUpdate = async (id, inicio, fin) => {
    setError("");
    try {
      await updateReserva(id, {
        inicio: new Date(inicio).toISOString(),
        fin: new Date(fin).toISOString(),
      });
      setMessage("Reserva actualizada");
      cargarReservas();
    } catch (err) {
      setError(err.message);
    }
  };

  const cargarNotis = async () => {
    try {
      const data = await getNotificaciones();
      setNotis(data);
    } catch (err) {}
  };

  return (
    <div className="sr-container">
      <h2 className="sr-title">Reservas del estudiante</h2>

      {message && <p className="sr-success">{message}</p>}
      {error && <p className="sr-error">{error}</p>}

      {/* Sección de Buscar + Crear juntos */}
      <div className="sr-row">
        {/* Buscar aulas */}
        <section className="sr-card small">
          <h3>Buscar aulas disponibles</h3>

          <form onSubmit={buscarDisponibles} className="sr-form">
            <label>
              Inicio
              <input
                type="datetime-local"
                value={filters.inicio}
                onChange={(e) =>
                  setFilters({ ...filters, inicio: e.target.value })
                }
                required
              />
            </label>

            <label>
              Fin
              <input
                type="datetime-local"
                value={filters.fin}
                onChange={(e) => setFilters({ ...filters, fin: e.target.value })}
                required
              />
            </label>

            <button className="sr-btn">Buscar</button>
          </form>

          {loadingDisponibles ? (
            <p>Cargando...</p>
          ) : (
            <div className="sr-aulas-grid">
              {disponibles.map((aula) => (
                <div key={aula.id_aula} className="sr-aula-card">
                  <strong>{aula.nombre_aula}</strong>
                  <p>Capacidad: {aula.capacidad}</p>
                  <button
                    className="sr-btn-secondary"
                    onClick={() => setForm({ ...form, id_aula: aula.id_aula })}
                  >
                    Seleccionar
                  </button>
                </div>
              ))}

              {disponibles.length === 0 && <p>Sin resultados</p>}
            </div>
          )}
        </section>

        {/* Crear reserva */}
        <section className="sr-card small">
          <h3>Crear reserva</h3>

          <form onSubmit={handleCreate} className="sr-form">
            <label>
              Inicio
              <input
                type="datetime-local"
                value={form.inicio}
                onChange={(e) =>
                  setForm({ ...form, inicio: e.target.value })
                }
                required
              />
            </label>

            <label>
              Fin
              <input
                type="datetime-local"
                value={form.fin}
                onChange={(e) =>
                  setForm({ ...form, fin: e.target.value })
                }
                required
              />
            </label>

            <label>
              Aula seleccionada
              <input
                value={form.id_aula}
                onChange={(e) =>
                  setForm({ ...form, id_aula: e.target.value })
                }
                required
                placeholder="ID de aula"
              />
            </label>

            <button className="sr-btn" disabled={loadingReserva}>
              {loadingReserva ? "Procesando..." : "Reservar"}
            </button>
          </form>
        </section>
      </div>

      {/* Mis reservas */}
      <section className="sr-card wide">
        <h3>Mis reservas</h3>

        {loading ? (
          <p>Cargando...</p>
        ) : reservas.length === 0 ? (
          <p>Aún no tienes reservas</p>
        ) : (
          <table className="sr-table">
            <thead>
              <tr>
                <th>Aula</th>
                <th>Inicio</th>
                <th>Fin</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {reservas.map((r) => (
                <tr key={r.id_reserva}>
                  <td>{r.aula?.nombre_aula}</td>

                  <td>
                    <input
                      type="datetime-local"
                      defaultValue={formatISO(r.inicio)}
                      onChange={(e) => (r._nuevoInicio = e.target.value)}
                    />
                  </td>

                  <td>
                    <input
                      type="datetime-local"
                      defaultValue={formatISO(r.fin)}
                      onChange={(e) => (r._nuevoFin = e.target.value)}
                    />
                  </td>

                  <td>{r.estado}</td>

                  <td>
                    <button
                      className="sr-btn-secondary"
                      onClick={() =>
                        handleUpdate(
                          r.id_reserva,
                          r._nuevoInicio || r.inicio,
                          r._nuevoFin || r.fin
                        )
                      }
                    >
                      Guardar
                    </button>

                    <button
                      className="sr-btn-danger"
                      onClick={() => handleCancel(r.id_reserva)}
                    >
                      Cancelar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      {/* Notificaciones */}
      <section className="sr-card wide">
        <div className="sr-noti-header">
          <h3>Notificaciones</h3>
          <button className="sr-btn-secondary" onClick={cargarNotis}>
            Refrescar
          </button>
        </div>

        <ul className="sr-noti-list">
          {notis.length === 0 ? (
            <li>Sin notificaciones</li>
          ) : (
            notis.map((n, idx) => <li key={idx}>{n.mensaje}</li>)
          )}
        </ul>
      </section>
    </div>
  );
}
