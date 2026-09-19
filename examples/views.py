from interlink import Generator, Tempulation, tempulator, templetonBP, url_not_found, internal_error, honeypot, backdoor, login, DB, site_map
from flask import Flask, Blueprint, render_template, url_for, request

viewsBP = Blueprint('/', __name__, url_prefix='/')

@viewsBP.route('/')
@honeypot
@backdoor
def index():
  domains = ['www.wormhole.click', 'www.prodoplanet.com', 'www.armyglass.org', 'www.maddiesmisccreations.com', 'www.joecorso.com', 'www.glassrage.com']
  #gitRepo = Generator('repository', 'DB_USER', 'DB_PASS')
  #manifest = gitRepo.generateQuery('qgitRepo1')
  #report = gitRepo.generateReport('qgitRepo1')
  manifest = "hi"
  siteMap = site_map()
  return render_template('index.html', siteMap=siteMap, domains=domains, manifest=manifest)

@viewsBP.route('/blog')
@honeypot
@backdoor
def blog():
  siteMap = site_map()
  return render_template('blog.html', siteMap=siteMap)

@viewsBP.route('/copyright')
@honeypot
@backdoor
def copyright():
  siteMap = site_map()
  return render_template('copyright.html', siteMap=siteMap)

@viewsBP.route('/repository')
@honeypot
@backdoor
def repository():
  siteMap = site_map()
  return render_template('index.html', siteMap=siteMap)
