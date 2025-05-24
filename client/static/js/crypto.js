// crypto.js

// Hàm ký dữ liệu bằng private key PEM (chuỗi)
function signData(privateKeyPEM, data) {
    const rsa = new RSAKey();
    rsa.readPrivateKeyFromPEMString(privateKeyPEM);

    // Tính SHA256 hash dữ liệu (string)
    const hashHex = KJUR.crypto.Util.sha256(data);

    // Ký hash
    const signatureHex = rsa.signHex(hashHex, "sha256");
    return signatureHex; // hex string
}

// Hàm verify chữ ký bằng public key PEM (chuỗi)
function verifySignature(publicKeyPEM, data, signatureHex) {
    const rsa = new RSAKey();
    rsa.readCertPEM(publicKeyPEM); // hoặc readPublicKeyFromPEMString

    const hashHex = KJUR.crypto.Util.sha256(data);

    return rsa.verifyHex(hashHex, signatureHex);
}

// Hàm mã hóa dữ liệu với public key (string) (dữ liệu không quá lớn)
function encryptWithPublicKey(publicKeyPEM, data) {
    const rsa = new RSAKey();
    rsa.readCertPEM(publicKeyPEM);

    // Mã hóa data (string) thành base64
    const encryptedB64 = rsa.encrypt(data);
    return encryptedB64;
}

// Hàm giải mã với private key (string)
function decryptWithPrivateKey(privateKeyPEM, encryptedB64) {
    const rsa = new RSAKey();
    rsa.readPrivateKeyFromPEMString(privateKeyPEM);

    const decrypted = rsa.decrypt(encryptedB64);
    return decrypted;
}
