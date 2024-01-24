USB_PORT    = /dev/ttyUSB0
CHIP        = esp32
BAUD        = 115200
BUFFER_SIZE = 30

AMPY_PORT = $(USB_PORT)
MICRO_PYTHON_BIN =  ./bin/micropython.bin
DOWNLOAD_FILES   := $(wildcard ./src/*)

default:reset

env:
	export AMPY_PORT=$(AMPY_PORT)

erase:
	esptool --port $(USB_PORT) erase_flash

flash: erase
	esptool --chip $(CHIP) --port $(USB_PORT) --baud $(BAUD) write_flash -z 0x1000 $(MICRO_PYTHON_BIN)


FINISH = $(patsubst %,./build/%.makeing,$(DOWNLOAD_FILES))
./build/%.makeing : % 
	touch $@
	echo $@
	
# ampy --port $(USB_PORT) put $<

$(FINISH):$(DOWNLOAD_FILES)

run:
	ampy --port $(AMPY_PORT) run  ./src/main.py


# download all the files in src
download:$(FINISH)
	

init:flash download

reset:
	ampy --port $(AMPY_PORT) reset
	ampy --port $(AMPY_PORT) put $(DOWNLOAD_FILES)
	ampy --port $(AMPY_PORT) run boot.py

shell:
	gnome-terminal -- bash -c "rshell --buffer-size=$(BUFFER_SIZE) -p $(USB_PORT);exec bash"

.PHONY:default erase flash init download reset shell
