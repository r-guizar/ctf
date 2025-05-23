#!/bin/sh

build_container() {
  echo -e "\e[1;34m[+] Building Challenge Docker Container\e[0m"
  docker build -t localhost/chall-genie_in_an_elf --platform linux/amd64 . 
}

run_container() {
  echo -e "\e[1;34m[+] Running Challenge Docker Container on 127.0.0.1:1337\e[0m"
  docker run --name chall-genie_in_an_elf --rm -p 127.0.0.1:1337:1337 -t -i -e HOST=127.0.0.1 -e PORT=1337 --user 1337:1337 --read-only --tmpfs /.cache:size=1M --security-opt=no-new-privileges:true --platform linux/amd64 localhost/chall-genie_in_an_elf
}

kill_container() {
	docker ps --filter "name=chall-genie_in_an_elf" --format "{{.ID}}" \
		| tr '\n' ' ' \
		| xargs docker stop -t 0 \
		|| true
}

case "${1}" in
  "build")
    build_container
    ;;
  "run")
    run_container
    ;;
  "kill")
    kill_container
    ;;
  *)
    build_container
    run_container
    ;;
esac
