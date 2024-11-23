import rsa 

public_key, private_key = rsa.newkeys(1024)

with open("./networking/keys/public.pem", "rb") as f:
    f.write(public_key.save_pkcs1("PEM"))

with open("./networking/keys/private.pem", "rb") as f:
    f.write(private_key.save_pkcs1("PEM"))


