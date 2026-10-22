{
  description = "Python ml flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs {
        inherit system;
        config.allowUnfree = true;
      };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          python3
          python3.pkgs.pip
          python3.pkgs.virtualenv
          
          graphviz
          stdenv.cc.cc.lib
          zlib
          glib
        ];

        shellHook = ''
          if [ ! -d ".venv" ]; then
            echo "Creating Python virtual environment (.venv)..."
            python -m venv .venv
          fi

          source .venv/bin/activate

          pip install --upgrade pip
          pip install \
            cvxopt \
            graphviz \
            ipython \
            ipythonblocks \
            ipywidgets \
            jupyter \
            keras \
            matplotlib \
            networkx \
            numpy \
            opencv-contrib-python \
            pandas \
            pillow \
            pytest \
            pytest-cov \
            qpsolvers \
            scipy \
            sortedcontainers \
            tensorflow
        '';
      };
    };
}
