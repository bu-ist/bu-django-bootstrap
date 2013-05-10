# Python
class python {
    package {
    	"build-essential": 		ensure => latest;
        "python": 				ensure => "2.6.5-0ubuntu1";
        "python-dev": 			ensure => "2.6.5-0ubuntu1";
        "python-setuptools":	ensure => "latest";
    }

	exec { "easy_install pip":					      
		path => "/usr/local/bin:/usr/bin:/bin",			     
		refreshonly => true,						
		require => Package["python-setuptools"],			    
		subscribe => Package["python-setuptools"],			  
	}	
	
    # Virtualenv, Fabric
    package { "virtualenv":
        ensure => "1.7.1.2",
        require => Exec["easy_install pip"],
        provider => pip;
    }
    package{ "fabric": 
        ensure => "0.9.3", 
        require => Exec["easy_install pip"],   
        provider => pip;
    }
}
