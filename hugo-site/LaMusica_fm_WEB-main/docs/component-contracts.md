# Contratos de componentes

## SiteHeader
- Logo enlazado a `/`.
- Navegación principal tomada de `content/site-content.json`.
- CTA persistente a `/contacto/`.
- En <=1080 px, reemplazar navegación por menú accesible.
- El botón del menú debe usar `aria-expanded`, controlar foco y cerrar con Escape.

## Hero
- Un solo H1.
- Eyebrow, título, texto, CTA principal y CTA secundario.
- El mapa visual de conexiones nunca puede reemplazar los enlaces textuales.

## NeedSelector
- Seis opciones tomadas de `services.needs`.
- Cada opción enlaza a una familia de servicios.
- En contacto, la selección viaja en la URL como `?need=<id>` y queda precargada.

## FamilyGrid y ServiceCard
- La familia muestra título, descripción y lista de servicios.
- Cada servicio muestra pregunta, resumen, entregables, precio o modalidad, límites y CTA.
- No renderizar campos vacíos.
- El CTA conserva `need`, `family` y `service` en la URL de contacto.

## EntityCard y ProjectCard
- Mostrar logo disponible, nombre, tipo, descripción y enlace.
- Resolver el logo desde `brandAssets`. Elegir `primary`, `dark` o `light` según el contraste del bloque.
- Mantener proporción, área libre y colores del archivo. No recortar, recolorear ni reconstruir.
- Si `externalUrl` es nulo, ocultar el enlace externo; nunca mostrar un botón inactivo.
- Los enlaces externos se identifican visualmente y abren en la misma pestaña salvo decisión del usuario.

## BrandSection
- Mantener navegación, retícula y tipografía funcional de LaMúsica.fm.
- Incorporar la identidad de la marca únicamente en el tramo que habla de ella.
- Para una sola marca: usar su logo y sus recursos como capa de contexto.
- Para varias marcas: separar cada identidad en su propio módulo y mostrar la relación mediante el sistema de conexiones de LaMúsica.fm.
- No crear degradados, paletas híbridas, logos compuestos ni fondos repetidos a partir de los logos.
- Si no existe un activo apropiado para el fondo, cambiar la superficie; no alterar el logo.

## MilestoneTimeline
- Orden cronológico.
- Navegable con teclado y legible sin animación.
- En móvil se convierte en una lista vertical.

## DocumentViewer
- Título, vista previa y enlace de descarga.
- El PDF debe ser accesible desde un enlace directo aunque el visor falle.

## ConnectionMap
- Vista visual por nodos y conexiones.
- Vista textual equivalente siempre disponible.
- Filtros: empresa, marca, proyecto, servicio y visión de ciudad.
- Los nodos solo se conectan cuando existe una relación cargada en los datos.

## GuidedContactForm
- Cuatro pasos más consentimiento.
- Validación en cliente y servidor.
- Estados: vacío, campo inválido, enviando, éxito y error recuperable.
- Conservar contexto recibido por query string.
- No exponer direcciones de correo ni credenciales en el cliente.

## MediaBlock
- Sin reproducción automática.
- Controles visibles, subtítulos cuando haya voz y transcripción cuando corresponda.
- Respetar `prefers-reduced-motion`.

## SiteFooter
- Navegación secundaria, razón social, NIT, dirección, privacidad y enlaces externos configurados.
