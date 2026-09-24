<?php
/**
 * Receptor del formulario de contacto.
 *
 * Se publica fuera del sitio estático, en /api/contacto del servidor.
 * Todo dato sensible llega por variable de entorno: aquí no hay correos,
 * credenciales ni llaves.
 *
 * Variables de entorno requeridas:
 *   LMFM_CONTACT_TO        destinatario de las notificaciones
 *   LMFM_CONTACT_FROM      remitente autenticado del servidor de correo
 *   LMFM_CONTACT_LOG       ruta del archivo de registro (fuera del docroot)
 *   LMFM_CONTACT_ORIGIN    origen permitido, por ejemplo https://lamusica.fm
 */

declare(strict_types=1);

const REQUIRED_FIELDS = ['profile', 'need', 'routeDetails', 'name', 'email', 'city', 'country', 'preferredChannel', 'privacy'];
const CONTEXT_FIELDS = ['need', 'family', 'service', 'route'];
const OPTIONAL_FIELDS = ['organization', 'whatsappOptional', 'relevantUrlOptional'];

/** Responde en JSON y termina la petición. */
function respond(int $status, array $payload): void
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($payload, JSON_UNESCAPED_UNICODE);
    exit;
}

/** Lee una variable de entorno obligatoria. */
function env(string $name): string
{
    $value = getenv($name);
    if ($value === false || $value === '') {
        error_log("contacto: falta la variable de entorno $name");
        respond(500, ['error' => 'El formulario no está configurado en el servidor.']);
    }
    return $value;
}

/** Limpia un valor recibido del formulario. */
function clean(string $value): string
{
    return trim(strip_tags($value));
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    respond(405, ['error' => 'Método no permitido.']);
}

$allowedOrigin = env('LMFM_CONTACT_ORIGIN');
$origin = $_SERVER['HTTP_ORIGIN'] ?? $allowedOrigin;
if (strpos($origin, $allowedOrigin) !== 0) {
    respond(403, ['error' => 'Origen no permitido.']);
}

// Trampa anti-spam: el campo está oculto para las personas.
if (clean((string)($_POST['website'] ?? '')) !== '') {
    respond(204, []);
}

$errors = [];
$data = [];

foreach (array_merge(REQUIRED_FIELDS, OPTIONAL_FIELDS, CONTEXT_FIELDS) as $field) {
    $data[$field] = clean((string)($_POST[$field] ?? ''));
}

foreach (REQUIRED_FIELDS as $field) {
    if ($data[$field] === '') {
        $errors[$field] = 'Este campo es obligatorio.';
    }
}

if ($data['email'] !== '' && !filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
    $errors['email'] = 'Escribe un correo electrónico válido.';
}

if ($data['privacy'] !== 'si') {
    $errors['privacy'] = 'Necesitamos tu autorización para tratar los datos.';
}

if ($errors) {
    respond(422, ['error' => 'Revisa los campos marcados.', 'fields' => $errors]);
}

$lines = ['Nueva consulta desde lamusica.fm', ''];
foreach ($data as $field => $value) {
    if ($value !== '') {
        $lines[] = "$field: $value";
    }
}
$lines[] = '';
$lines[] = 'IP: ' . ($_SERVER['REMOTE_ADDR'] ?? 'desconocida');
$body = implode("\n", $lines);

$sent = mail(
    env('LMFM_CONTACT_TO'),
    'Consulta web · ' . ($data['need'] ?: 'sin ruta'),
    $body,
    implode("\r\n", [
        'From: ' . env('LMFM_CONTACT_FROM'),
        'Reply-To: ' . $data['email'],
        'Content-Type: text/plain; charset=utf-8',
    ])
);

// El registro permite recuperar una consulta si el correo falla.
$logPath = getenv('LMFM_CONTACT_LOG');
if ($logPath) {
    file_put_contents($logPath, date('c') . ' ' . json_encode($data, JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND | LOCK_EX);
}

if (!$sent) {
    error_log('contacto: mail() falló');
    respond(502, ['error' => 'No pudimos enviar el mensaje. Intenta de nuevo.']);
}

respond(200, ['ok' => true]);
