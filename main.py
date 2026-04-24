import math
import matplotlib.pyplot as plt
import glob
import imageio.v2 as imageio

def main():

    n=35
    numbers= list(range(2,n+1))
    print(numbers)
    prime_flag= {x: True for x in numbers}
    print (prime_flag)
    states = sieve(n, numbers, prime_flag)

    for idx, state in enumerate(states, start=1):
        filename = f"frame_{idx:03d}.png"
        draw_frame(
            numbers,
            state["flags"],
            state["marked_number"],
            current_prime=state["current_prime"],
            filename=filename
        )
    build_gif()

def sieve(n,numbers,prime_flag):
    states = []
    for p in numbers:
        if p * p > n: # to stop the first number loop as it is no point to continue if x^y is greater than largest number
            break
        if prime_flag[p]:
            print("Current prime:", p)
             # optional announcement frame
            states.append({
                "current_prime": p,
                "marked_number": None,
                "flags": prime_flag.copy()
            })
            for i in range(p*p, n + 1, p):
                if prime_flag[i]:
                    prime_flag[i]=False
                states.append({
                    "current_prime": p,
                    "marked_number":i,
                    "flags": prime_flag.copy()
                })
    return states

def draw_frame(numbers,prime_flag,marked_number,current_prime,filename):
    cols=6
    rows=math.ceil(len(numbers)/cols)
    fig,ax=  plt.subplots(figsize=(8, 8))
    ax.set_xlim(0,cols)
    ax.set_ylim(0,rows+1.5)
    ax.axis("off")

    ax.text(cols/2,rows+1, "Sieve of Eratosthenes", ha="center",va="center",fontsize=18,fontweight="bold")

    ax.text(cols/2, rows+0.5,f"Current Primt:{current_prime}", ha="center",va="center",fontsize=12)

    for idx,number in enumerate(numbers):
        row= idx // cols
        col=idx % cols

        x= col + 0.5
        y=rows -row

        if number == current_prime:
            ax.text(x, y, str(number), ha="center", va="center", fontsize=14, color="blue", fontweight="bold")
        elif number == marked_number:
            ax.text(x, y, str(number), ha="center", va="center", fontsize=14, color="red", fontweight="bold")
        elif not prime_flag[number]:
            ax.text(x, y, str(number), ha="center", va="center",
            fontsize=14, color="gray", alpha=0.35)
        else:
            ax.text(x, y, str(number), ha="center", va="center",
            fontsize=14, color="black")
            
    plt.savefig(filename,dpi=150, bbox_inches="tight")
    plt.close()

def build_video(output_name="sieve_animation.mp4", fps=1):
    frame_files = sorted(glob.glob("frame_*.png"))

    with imageio.get_writer(output_name, fps=fps) as writer:
        for file in frame_files:
            image = imageio.imread(file)
            writer.append_data(image)

    print(f"Video created: {output_name}")

def build_gif(output_name="sieve_animation.gif", fps=1):
    frame_files = sorted(glob.glob("frame_*.png"))

    with imageio.get_writer(output_name, mode="I", duration=1/fps) as writer:
        for file in frame_files:
            image = imageio.imread(file)
            writer.append_data(image)

    print(f"GIF created: {output_name}")

if __name__ == "__main__":
    main()