#!/bin/bash

makeAppFactory(){
  # Make an app factory
  base_dir=$(dirname "$(readlink -f "${0%/*}")")
  mkdir -p "${base_dir}/tests/app_factory/{log,run,static/{css/{base,components,theme},js,img/{icons,logos,banners,products,backgrounds},templates/includes}"
}

makeFrontEnd(){
  # Make a frontend framework
  base_dir=$(dirname "$(readlink -f "${0%/*}")")
  mkdir "${base_dir}/tests/webFrontEnd/{static/{css/{base,components,theme},js,img/{icons,logos,banners,products,backgrounds}},templates/includes}"
}