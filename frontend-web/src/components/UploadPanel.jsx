export default function UploadPanel({ onFile }) {
  return (
    <input
      type="file"
      accept="image/*"
      onChange={(e) => onFile(e.target.files[0])}
      className="border p-2 rounded w-full"
    />
  );
}
