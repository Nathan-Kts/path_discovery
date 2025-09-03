Set up the online boutique witout load generator:
```
docker compose up -d
```

Find the PID of a container [for example the front end container]
```
sudo docker ps
sudo docker top < front-end id >
```

Starting Prism:
```
sudo docker run \
    --rm -it --privileged \
    -e RUST_LOG=info \
    --pid host \
    -v "$(pwd)"/cdata:/data \
    -v /sys/fs/cgroup:/sys/fs/cgroup \
    -v /sys/kernel/tracing:/sys/kernel/tracing \
    -v /sys/kernel/debug:/sys/kernel/debug \
    --name prism \
    dclandau/prism:latest --machine-id 1 --pids 13019
```

Start the 


# Experiment 4: Illustration

Make sure you have started the k8s version of the online boutique microservices from the first experiment, and that you have portforwarded the frontend to your local 8080 port.

Build the load generator: 
```bash
docker build -t custom-ob-lg .
```

Run the load generator
```bash
docker run -v $(pwd)/results:/loadgen/results --network host --entrypoint locust custom-ob-lg --headless -t 5m -u 1 --csv results/load --csv-full-history --host http://localhost:8080
```




# Processing data
The following command will extract the .db3 file and create csv files corresponding to the different tables.
```
python3 db3toCSV.py
```

Extraction of the inode partners:
```
python3 inode_partner_search.py temp_work_folder/tcp_discovery.csv
```