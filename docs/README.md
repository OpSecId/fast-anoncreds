# Fast AnonCreds
[Gotta Go Fast!](https://www.youtube.com/watch?v=Z9G1Mf6TZRs)

There's also the [OpenAPI web page](https://fast.anoncreds.vc/docs) available!

## Creating AnonCreds Objects
Please be patient when creating objects.

### Minimal Example
```bash
curl -X 'POST' \
  'https://fast.anoncreds.vc' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{}' | jq .

```

### Extended Example
```bash
curl -X 'POST' \
  'https://fast.anoncreds.vc' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
        "name": "Person",
        "attributes": ["givenName", "familyName"],
        "size": 1000,
        "revocation": true
      }' | jq .

```