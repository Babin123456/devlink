/**
 * Spanish catalogue.
 *
 * Included as a worked reference so the shape of a second locale is concrete
 * rather than hypothetical. Deliberately *not* exhaustive: the missing keys
 * demonstrate that an incomplete catalogue falls back to English cleanly
 * instead of rendering a raw key at the user.
 */

import type { Catalogue } from "../types";

export const es: Catalogue = {
  "common.appName": "DevLink",
  "common.cancel": "Cancelar",
  "common.save": "Guardar",
  "common.retry": "Reintentar",
  "common.goHome": "Ir al inicio",
  "common.goBack": "Volver",
  "common.goToLogin": "Iniciar sesión",
  "common.loading": "Cargando…",
  "common.search": "Buscar",
  "common.close": "Cerrar",

  "errors.unauthorized.title": "401 • No autorizado",
  "errors.unauthorized.description": "Debes iniciar sesión para acceder a esta página.",

  "errors.forbidden.title": "403 • Prohibido",
  "errors.forbidden.description": "No tienes permiso para acceder a este recurso.",

  "errors.serverError.title": "500 • Error del servidor",
  "errors.serverError.description":
    "Algo salió mal por nuestra parte. Inténtalo de nuevo en unos momentos.",

  "errors.network.title": "Error de red",
  "errors.network.description": "No pudimos conectar con el servidor. Inténtalo de nuevo.",

  "errors.offline.title": "Estás sin conexión",
  "errors.offline.description": "Comprueba tu conexión a internet e inténtalo de nuevo.",

  "language.label": "Idioma",
  "language.change": "Cambiar idioma",

  "projects.count": {
    one: "{count} proyecto",
    other: "{count} proyectos",
  },
  "members.count": {
    one: "{count} miembro",
    other: "{count} miembros",
  },
  // "notifications.unread" is intentionally absent — it falls back to English.
};

export default es;
