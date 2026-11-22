/* Point d'entrée du paquet navigateur vendor/blob-upload.js (envoi direct vers Vercel Blob).
   Reconstruire : bash tools/contrib/build_blob_client.sh */
import { upload } from "@vercel/blob/client";
window.OnrecordBlob = { upload: upload };
