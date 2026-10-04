# Correctif de compatibilité pour la prévisualisation LOCALE du site.
#
# Liquid 4.0.3 (version épinglée par le méta-gem `github-pages`) appelle
# encore `Object#tainted?`, retiré depuis Ruby 3.2. Sur un Ruby récent
# (ex. Homebrew ruby 4.x), le build local échoue sans ce shim.
#
# Usage :
#   RUBYOPT="-r$PWD/script/ruby_compat.rb" bundle exec jekyll serve
#
# GitHub Pages n'a PAS besoin de ce fichier : son environnement fournit
# lui-même la combinaison de versions qui fonctionne.
unless Object.method_defined?(:tainted?)
  class Object
    def tainted?; false; end
    def taint; self; end
    def untaint; self; end
  end
end
