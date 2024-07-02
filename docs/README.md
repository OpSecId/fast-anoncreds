# Fast AnonCreds
[Gotta Go Fast!](https://www.youtube.com/watch?v=Z9G1Mf6TZRs)

## Creating AnonCreds Objects
```bash
curl -X 'POST' \
  'https://fast.anoncreds.vc' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{}' | jq .

```

## Setup parameters
```json
{
    // schema name
    "name": "example",
    // schema attributes
    "attributes": [],
    // revocation registry size
    "size": 10,
    // create revocation registry object
    "revocation": false,
    // publish verification document
    "publish": false
}
```