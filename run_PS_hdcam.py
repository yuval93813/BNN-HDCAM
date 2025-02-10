import pyvisa
from time import sleep

#script paired with edram_cdf_demo.c to init cdf graph preview

# consts:
ch_vref = 'ch1'
ch_veval = 'ch2'
ch_vrep = 'ch3'
vltg_change_delay = 0.05

class run_class:

    PS_address = 'USB0::0x1AB1::0x0E11::DP8C163852776::0::INSTR'
    
    def __init__(self,serGW) :
        print("run_PS_hdcam.py : Constructing hpx object")
        self.serGW = serGW
        self.test_idx = 0
        self.rm = pyvisa.ResourceManager()


    def init_PS(self):
        self.SUPPLY = self.rm.open_resource(self.PS_address)
        sleep(vltg_change_delay)
        self.set_veval(0)
        self.set_vref(0)
        self.set_vrep(0)

        #check if supply is on:
        if not (self.ch_on(ch_veval) and self.ch_on(ch_vref) and self.ch_on(ch_vrep)):
            print("ERROR: output is off")
            self.close_PS()
            exit()


    def ch_on(self,ch_str):
        state=self.SUPPLY.query(f":output? {ch_str}")
        return (True if state=='ON\n' else False)

    def close_PS(self):
        print("Closing instrumants")
        """shutting off supply:"""
        self.set_veval(0)
        self.set_vref(0)
        self.set_vrep(0)
        """close instruments:"""
        self.SUPPLY.write('SYSTEM:local')
        sleep(vltg_change_delay)
        self.SUPPLY.close()
        sleep(vltg_change_delay)
        self.rm.close()

    def set_veval(self,v_veval):
        self.set_v(ch_veval, str(v_veval / 1000))

    def set_vref(self, v_vref):
        self.set_v(ch_vref,str(v_vref / 1000))

    def set_vrep(self, v_vrep):
        self.set_v(ch_vrep,str(v_vrep / 1000))

    def set_v(self,ch_str, voltage):
        self.SUPPLY.write("apply " + ch_str + "," + voltage)  # change voltage
        sleep(vltg_change_delay)
        
if __name__=="__main__":
    a=run_class(0)
    print(a)
    a.init_PS()
    # a.set_vref(100)
    # input("next?")
    # a.set_vref(110)
    # input("next?")
    # a.set_vref(120)
    # input("next?")
    # a.set_vref(130)
    # input("next?")
    a.set_vref(800)
    a.set_veval(900)
    a.set_vrep(1000)
    input("finish?")
    a.close_PS()
   