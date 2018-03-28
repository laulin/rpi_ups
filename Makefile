install:
	@mkdir /opt/rpi_ups
	@cp ls_ups.py /opt/rpi_ups/ls_ups.py && chmod a+x /opt/rpi_ups/ls_ups.py
	@cp raspi_ups_hat_interface.py /opt/rpi_ups/raspi_ups_hat_interface.py
	@cp watch_ups.py /opt/rpi_ups/watch_ups.py  && chmod a+x /opt/rpi_ups/watch_ups.py
	@ln -s /opt/rpi_ups/ls_ups.py /usr/local/bin/ls_ups
	@ln -s /opt/rpi_ups/watch_ups.py /usr/local/bin/watch_ups

uninstall:
	@rm -rf /opt/rpi_ups/
	@rm /usr/local/bin/ls_ups
	@rm /usr/local/bin/watch_ups