mermaids := $(wildcard *.mmd)
graphs := $(patsubst %.mmd,%.png,$(mermaids))

.PHONY : render clean

all: clean render open

render : $(graphs)

clean:
	rm -f *.png

open:
	open *.png

%.png: $@
	mmdc -c config.json -i $(patsubst %.png,%.mmd,$@) -o $@
