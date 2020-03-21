## Container build
```bash
docker build -t qr-decode .
```
## Container launch
```bash
docker run --rm -p 8000:80 -it qr-decode
```

## dotenv .env
```
HTTP_PORT=8000
HTTP_HOST=0.0.0.0
```

## Notes
```sh
curl --location --request POST '0.0.0.0:8000' \
--header 'Content-Type: multipart/form-data; boundary=--------------------------629486235723262203439969' \
--form 'scan=@/tmp/file.pdf'
```
