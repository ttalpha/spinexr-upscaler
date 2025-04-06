export function formatFileSize(bytes: number): string {
  const sizes = ["bytes", "KB", "MB", "GB", "TB"];
  if (bytes === 0) return "0 byte";
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  return parseFloat((bytes / Math.pow(1024, i)).toFixed(2)) + " " + sizes[i];
}
