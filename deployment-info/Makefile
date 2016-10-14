
all: dev-phet rc-phet release-phet dev-io rc-io release-io
PHONY: all

dev-phet: deploy-dev-phet.md

rc-phet: deploy-rc-phet.md

release-phet: deploy-release-phet.md

dev-io: deploy-dev-phet-io.md

rc-io: deploy-rc-phet-io.md

release-io: deploy-release-phet-io.md

deploy-dev-phet.md:
	cat src/preamble.md \
	 src/build-process-configuration.md \
	 src/dev-phet.md > doc/deploy-dev-phet.md

deploy-rc-phet.md:
	cat src/preamble.md \
	 src/build-process-configuration.md \
	 src/rc-phet.md > doc/deploy-rc-phet.md

deploy-release-phet.md:
	cat src/preamble.md \
	 src/build-process-configuration.md \
	 src/release-phet.md > doc/deploy-release-phet.md

deploy-dev-phet-io.md:
	cat src/preamble.md \
	 src/build-process-configuration.md \
	 src/dev-phet-io.md \
	 src/phet-io-testing.md > doc/deploy-dev-phet-io.md

deploy-rc-phet-io.md:
	cat src/preamble.md \
	 src/build-process-configuration.md \
	 src/rc-phet-io.md \
	 src/phet-io-testing.md > doc/deploy-rc-phet-io.md

deploy-release-phet-io.md:
	cat src/preamble.md \
	 src/build-process-configuration.md \
	 src/release-phet-io.md \
	 src/phet-io-testing.md > doc/deploy-release-phet-io.md

clean:
	rm doc/*.md
