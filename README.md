# Indy node monitoring

Please take a look at the corresponding blog entry: https://juanjo.garciaamaya.com/devops/indy-node-monitoring

This code is based on [BCgov's von-network](https://github.com/bcgov/von-network) work with minor additions ans was created for training purposes, not for production use.

# Running the example
If you want to run the example environment, do the following.

1. Clone this repository

```sh
git clone https://github.com/juanjo-vlc/hyperledger-indy-monitoring.git
```

2. CD into the projects folder
```sh
cd hyperledger-indy-monitoring
```

3. Copy the ```env.sample``` file to `.env`
```sh
cp env.sample .env
```

4. Edit the .env file using your favorite text editor and point the GENESIS_URL variable to point to your indy network's pool genesis url. As this was done for training, it uses the default Network DIDs, if you want to connect to your custom chain, edit the SEED environment variable to match the seed from DID with NETWORK_MONITOR role.

5. Bring up the containers
```sh
docker-compose up -d
```

Then you can point your browser to:
 * http://localhost:8000 BCGov's Ledger Browser to view basic information about the blockchain. The ledger navigation was disabled.
 * http://localhost:9090 Prometheus interface
 * http://localhost:3000 Grafana interface with default admin/admin authentication.

 As this was done for training, it uses the default Sovrin Builder's Network DIDs, if you want to connect to your custom chain, add the SEED environment variable to the browser container on the ```docker-compose.yml``` file.
