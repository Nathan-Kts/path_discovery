Set up the online boutique witout load generator.


Starting Prism:

docker run \
    --rm -it --privileged \
    -e RUST_LOG=info \
    --pid host \
    -v "$(pwd)"/cdata:/data \
    -v /sys/fs/cgroup:/sys/fs/cgroup \
    -v /sys/kernel/tracing:/sys/kernel/tracing \
    -v /sys/kernel/debug:/sys/kernel/debug \
    --name prism \
    dclandau/prism:latest --machine-id 1 --pids 3331592

    Replace the 3331592 with the PID of the frontend




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
