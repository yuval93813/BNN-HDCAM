import tkinter as tk
from tkinter import messagebox
from hdcamV2 import XBOX, Controller as HDCAM  # Import both XBOX and HDCAM
from run_PS_hdcam import run_class  # Power supply controller
import random

# Initialize the power supply once
ps_controller = run_class(0)
ps_controller.init_PS()

# Global variables to store last written data
last_written_xbox_data = None
last_written_hdcam_data = None

def get_random_data(size):
    """Generate random 64-bit data."""
    return [random.randint(0, (1 << 64) - 1) for _ in range(size)]

def open_xbox():
    """Initialize XBOX safely."""
    return XBOX(null_value=0x0)

def open_hdcam():
    """Initialize HDCAM safely."""
    return HDCAM()

def write_to_xbox():
    """Write data to XBOX."""
    global last_written_xbox_data
    try:
        xbox = open_xbox()
        data = get_random_data(480)
        xbox.write(data)
        last_written_xbox_data = data
        messagebox.showinfo("Success", "Data written to XBOX successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to write to XBOX: {e}")
    finally:
        try:
            if xbox.serial_gateway.serPort.is_open:
                xbox.serial_gateway.serPort.close()
        except AttributeError:
            print("XBOX serial port not available for closing.")

def read_from_xbox():
    """Read data from XBOX and compare with the last write."""
    try:
        xbox = open_xbox()
        read_data = read_from_xbox_memory(xbox)
        if read_data == last_written_xbox_data:
            messagebox.showinfo("Success", "XBOX data matches the last write.")
        else:
            messagebox.showerror("Error", "XBOX data mismatch detected!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read from XBOX: {e}")
    finally:
        try:
            if xbox.serial_gateway.serPort.is_open:
                xbox.serial_gateway.serPort.close()
        except AttributeError:
            print("XBOX serial port not available for closing.")

def read_from_xbox_memory(xbox):
    """Read data from XBOX SRAM."""
    read_data = []
    xbox_mem_ptr = xbox.xbox_mem_base_addr

    for _ in range(480):
        lsb = xbox.serial_gateway.rd_mem_by_uart(xbox_mem_ptr)
        msb = xbox.serial_gateway.rd_mem_by_uart(xbox_mem_ptr + 4)
        word = (msb << 32) | lsb
        read_data.append(word)
        xbox_mem_ptr += 8

    return read_data

def write_to_hdcam():
    """Write data to HDCAM."""
    global last_written_hdcam_data
    try:
        hdcam = open_hdcam()
        data = get_random_data(120)
        data = data*4
        hdcam.write(data)
        last_written_hdcam_data = data
        messagebox.showinfo("Success", "Data written to HDCAM successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to write to HDCAM: {e}")

def compare_hdcam_with_errors():
    """Compare HDCAM data with configurable bit errors."""
    global last_written_hdcam_data
    try:
        num_errors = int(entry_num_errors.get())
        corrupted_data = insert_bit_errors(last_written_hdcam_data, num_errors)

        hdcam = open_hdcam()
        correct_matches=hdcam.read(corrupted_data)

        match_percentage = (correct_matches / len(corrupted_data)) * 100

        messagebox.showinfo("Comparison Result", f"{match_percentage:.2f}% of rows matched with errors.")
    except ValueError:
        messagebox.showerror("Input Error", "Enter a valid number of bit errors.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to compare HDCAM: {e}")

def insert_bit_errors(data, num_errors):
    """Insert bit errors into data."""
    corrupted_data = []
    for word in data:
        corrupted_word = word
        for _ in range(num_errors):
            bit_to_flip = 1 << random.randint(0, 63)
            corrupted_word ^= bit_to_flip
        corrupted_data.append(corrupted_word)
    return corrupted_data

def apply_voltages():
    """Apply voltage settings."""
    try:
        vref = float(entry_vref.get())
        veval = float(entry_veval.get())
        vrep = float(entry_vrep.get())
        ps_controller.set_vref(vref)
        ps_controller.set_veval(veval)
        ps_controller.set_vrep(vrep)
        messagebox.showinfo("Success", "Voltages applied successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to apply voltages: {e}")

def on_closing():
    """Close the GUI and release resources."""
    try:
        ps_controller.close_PS()
    except Exception as e:
        print(f"Error during shutdown: {e}")
    finally:
        root.destroy()

# GUI Setup
root = tk.Tk()
root.title("HDCAM and XBOX Controller")

# Input Fields
tk.Label(root, text="Vref (mV):").grid(row=0, column=0, padx=10, pady=10)
entry_vref = tk.Entry(root)
entry_vref.grid(row=0, column=1)

tk.Label(root, text="Veval (mV):").grid(row=1, column=0, padx=10, pady=10)
entry_veval = tk.Entry(root)
entry_veval.grid(row=1, column=1)

tk.Label(root, text="Vrep (mV):").grid(row=2, column=0, padx=10, pady=10)
entry_vrep = tk.Entry(root)
entry_vrep.grid(row=2, column=1)

tk.Label(root, text="Bit Errors:").grid(row=3, column=0, padx=10, pady=10)
entry_num_errors = tk.Entry(root)
entry_num_errors.grid(row=3, column=1)

# Buttons
tk.Button(root, text="Write to XBOX", command=write_to_xbox).grid(row=4, column=0, padx=10, pady=10)
tk.Button(root, text="Read from XBOX", command=read_from_xbox).grid(row=4, column=1, padx=10, pady=10)
tk.Button(root, text="Write to HDCAM", command=write_to_hdcam).grid(row=5, column=0, padx=10, pady=10)
tk.Button(root, text="Compare HDCAM with Errors", command=compare_hdcam_with_errors).grid(row=5, column=1, padx=10, pady=10)
tk.Button(root, text="Apply Voltages", command=apply_voltages).grid(row=6, column=0, columnspan=2, pady=10)

# Close event binding
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the GUI event loop
root.mainloop()
