
# First two files in every concatenation
INTRO = src/preamble.md src/build-process-configuration.md

TEST_IO = src/phet-io-testing.md

# Common dependencies: if these change, rebuild whatever depends on them
DEPS = Makefile $(INTRO)

# Default target
all: phet phet-io

phet: \
	doc/deploy-dev-phet.md \
	doc/deploy-rc-phet.md \
	doc/deploy-release-phet.md

phet-io: \
	doc/deploy-dev-phet-io.md \
	doc/deploy-rc-phet-io.md \
	doc/deploy-release-phet-io.md

# These targets do not have corresponding file names
PHONY: all clean phet phet-io

# Individual markdown file targets, dependencies, and build rules
doc/deploy-dev-phet.md: $(DEPS) src/dev-phet.md
	cat $(INTRO) src/dev-phet.md > $@

doc/deploy-rc-phet.md: $(DEPS) src/rc-phet.md
	cat $(INTRO) src/rc-phet.md > $@

doc/deploy-release-phet.md: $(DEPS) src/release-phet.md
	cat $(INTRO) src/release-phet.md > $@

doc/deploy-dev-phet-io.md: $(DEPS) $(TEST_IO) src/dev-phet-io.md
	cat $(INTRO) src/dev-phet-io.md $(TEST_IO) > $@

doc/deploy-rc-phet-io.md: $(DEPS) $(TEST_IO) src/rc-phet-io.md
	cat $(INTRO) src/rc-phet-io.md $(TEST_IO) > $@

doc/deploy-release-phet-io.md: $(DEPS) $(TEST_IO) src/release-phet-io.md
	cat $(INTRO) src/release-phet-io.md $(TEST_IO) > $@

clean:
	rm doc/*.md
