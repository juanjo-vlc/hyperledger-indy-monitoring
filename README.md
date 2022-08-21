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

4. Edit the .env file using your favorite text editor and point the GENESIS_URL variable to point to your indy network's pool genesis url.
