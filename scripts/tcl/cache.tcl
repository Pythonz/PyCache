namespace eval cache {
	proc connect {{ip "127.0.0.1"} {port "1270"}} {
		if {![info exists ::pyca]} {
			set ::pyca [socket $ip $port]
		}
	}

	proc stor {str data} {
		if {[info exists ::pyca]} {
			puts $::pyca "STOR $str $data"
			flush $::pyca
			gets $::pyca line
			if {$line == "OK"} {
				return 1
			}
		}
		return 0
	}

	proc retr {str} {
		if {[info exists ::pyca]} {
			puts $::pyca "RETR $str"
			flush $::pyca
			gets $::pyca line
			if {$line != "ERROR"} {
				return [lrange $line 2 end]
			}
		}
		return 0
	}

	proc drop {str} {
		if {[info exists ::pyca]} {
			puts $::pyca "DROP $str"
			flush $::pyca
			gets $::pyca line
			if {$line == "OK"} {
				return 1
			}
		}
		return 0
	}

	proc rena {str newstr} {
		if {[info exists ::pyca]} {
			puts $::pyca "RENA $str $newstr"
			flush $::pyca
			gets $::pyca line
			if {$line == "OK"} {
				return 1
			}
		}
		return 0
	}

	proc exis {str} {
		if {[info exists ::pyca]} {
			puts $::pyca "EXIS $str"
			flush $::pyca
			gets $::pyca line
			if {$line == "OK"} {
				return 1
			}
		}
		return 0
	}

	proc line {integer} {
		if {[info exists ::pyca]} {
			puts $::pyca "LINE $integer"
			flush $::pyca
			gets $::pyca line
			if {$line == "OK"} {
				return 1
			}
		}
		return 0
	}

	proc dele {} {
		if {[info exists ::pyca]} {
			puts $::pyca "DELE"
			flush $::pyca
			gets $::pyca line
			if {$line == "OK"} {
				return 1
			}
		}
		return 0
	}

	proc quit {} {
		if {[info exists ::pyca]} {
			puts $::pyca "QUIT"
			flush $::pyca
			gets $::pyca line
			if {$line == "OK"} {
				close $::pyca
				unset ::pyca
				return 1
			}
		}
		return 0
	}

	proc shutdown {} {
		if {[info exists ::pyca]} {
			close $::pyca
			unset ::pyca
		}
	}

	proc reconnect {{ip "127.0.0.1"} {port "1270"}} {
		if {[info exists ::pyca]} {
			close $::pyca
			unset ::pyca
		}
		if {![info exists ::pyca]} {
			set ::pyca [socket $ip $port]
		}
	}

	proc status {} {
		if {[info exists ::pyca]} {
			return 1
		}
		return 0
	}
}
