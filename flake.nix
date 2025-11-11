{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.git-hooks.url = "github:cachix/git-hooks.nix";

  outputs = inputs @ {self, ...}:
    inputs.flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = inputs.nixpkgs.legacyPackages.${system};

        pre-commit-check = inputs.git-hooks.lib.${system}.run {
          src = ./.;
          hooks = {
            alejandra.enable = true;
            ruff.enable = true;
            ruff-format.enable = true;
            # unit-tests = {
            #   enable = true;
            #   entry = "bash -c 'cd backend && bash ./scripts/tests-start.sh'";
            #   files = "^backend/";
            #   pass_filenames = false;
            # };
            bun-precommit = {
              enable = true;
              entry = "bash -c 'cd frontend && bun run precommit'";
              files = "^frontend/";
              pass_filenames = false;
            };
          };
        };

        nativeBuildInputs = with pkgs; [
          uv
          python3
          djlint
          ruff
          bun
        ];

        buildInputs = with pkgs; [];
      in {
        devShells.default = pkgs.mkShell {
          inherit nativeBuildInputs;
          shellHook = pre-commit-check.shellHook;
          buildInputs = buildInputs ++ pre-commit-check.enabledPackages;
        };

        formatter = let
          config = pre-commit-check.config;
          inherit (config) package configFile;
          script = ''
            ${pkgs.lib.getExe package} run --all-files --config ${configFile}
          '';
        in
          pkgs.writeShellScriptBin "pre-commit-run" script;

        packages.default = pkgs.stdenv.mkDerivation {
          pname = "apartments";
          version = "0.0.0";
          src = ./.;

          nativeBuildInputs =
            nativeBuildInputs
            ++ [
            ];
          inherit buildInputs;
        };
      }
    );
}
