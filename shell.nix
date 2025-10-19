with import <nixpkgs> {}; let
  inherit (llvmPackages_latest) stdenv clang bintools;
in
  mkShell.override {inherit stdenv;} {
    nativeBuildInputs = [
      clang
      bintools
    ];
    CXXFLAGS = "-O3 -pipe -mcpu=native";
    LDFLAGS = "-fuse-ld=lld -flto=thin";

    NIX_ENFORCE_NO_NATIVE = 0;

    hardeningDisable = ["all"];
  }
