import { motion, Variants } from "framer-motion";
import styled from "styled-components";

const Logo = styled(motion.svg)`
  background-color: white;
  width: 500px;
  height: 200px;
`;
const logoVariants: Variants = {
  initial: {
    pathLength: 0,
    fill: "transparent",
    strokeWidth: "2",
    stroke: "#000000",
    vectorEffect: "non-scaling-stroke",
    d: "M 29.55 0 L 36.6 27.9 L 37 27.9 Q 38.65 20.85 40.35 14 Q 42.05 7.15 43.8 0 L 51.4 0 L 40.9 42.55 L 32.75 42.55 L 25.75 15.15 L 19 42.55 L 10.85 42.55 L 0 0 L 7.65 0 L 14.7 27.9 L 15.1 27.9 L 16.75 21.1 Q 18.05 15.8 19.325 10.575 Q 20.6 5.35 21.9 0 L 29.55 0 Z M 69.15 17.85 L 67.6 17.85 Q 66.441 17.85 65.59 18.048 A 4.838 4.838 0 0 0 64.925 18.25 A 4.582 4.582 0 0 0 64.114 18.658 A 3.355 3.355 0 0 0 63.325 19.35 A 3.682 3.682 0 0 0 62.638 20.669 A 4.448 4.448 0 0 0 62.55 21.025 A 9.925 9.925 0 0 0 62.363 22.55 A 11.595 11.595 0 0 0 62.35 23.1 L 62.35 42.55 L 55.35 42.55 L 55.35 0 L 62.35 0 L 62.35 11.4 A 12.165 12.165 0 0 1 63.658 11.047 A 14.484 14.484 0 0 1 64.3 10.925 A 13.08 13.08 0 0 1 66.072 10.756 A 14.753 14.753 0 0 1 66.5 10.75 L 70.25 10.75 A 13.944 13.944 0 0 1 72.685 10.953 A 10.527 10.527 0 0 1 75.1 11.675 A 10.721 10.721 0 0 1 77.503 13.117 A 9.417 9.417 0 0 1 78.6 14.15 Q 80 15.7 80.7 17.65 Q 81.4 19.6 81.4 21.6 L 81.4 42.55 L 74.35 42.55 L 74.35 23.1 A 10.814 10.814 0 0 0 74.255 21.647 A 9.334 9.334 0 0 0 74.15 21.025 A 4.044 4.044 0 0 0 73.78 19.964 A 3.541 3.541 0 0 0 73.375 19.35 Q 72.8 18.65 71.8 18.25 Q 70.8 17.85 69.15 17.85 Z M 132.3 17.85 L 130.8 17.85 Q 129.641 17.85 128.79 18.048 A 4.838 4.838 0 0 0 128.125 18.25 A 4.582 4.582 0 0 0 127.314 18.658 A 3.355 3.355 0 0 0 126.525 19.35 A 3.682 3.682 0 0 0 125.838 20.669 A 4.448 4.448 0 0 0 125.75 21.025 A 9.925 9.925 0 0 0 125.563 22.55 A 11.595 11.595 0 0 0 125.55 23.1 L 125.55 42.55 L 118.2 42.55 L 118.2 10.75 L 125.55 10.75 L 125.55 11.55 A 12.921 12.921 0 0 1 129.351 10.774 A 15.088 15.088 0 0 1 130.2 10.75 L 133.45 10.75 A 13.921 13.921 0 0 1 136.025 10.978 A 10.698 10.698 0 0 1 138.325 11.675 A 10.982 10.982 0 0 1 140.708 13.076 A 9.599 9.599 0 0 1 141.875 14.15 Q 143.3 15.7 144.025 17.65 Q 144.75 19.6 144.75 21.6 L 144.75 42.55 L 137.4 42.55 L 137.4 23.1 A 12.337 12.337 0 0 0 137.317 21.647 A 10.562 10.562 0 0 0 137.225 21.025 A 4.036 4.036 0 0 0 136.909 20.015 A 3.449 3.449 0 0 0 136.5 19.35 A 3.245 3.245 0 0 0 135.663 18.608 A 4.44 4.44 0 0 0 134.95 18.25 Q 133.95 17.85 132.3 17.85 Z M 239 35.4 L 240.4 35.4 A 11.289 11.289 0 0 0 241.398 35.359 Q 241.883 35.316 242.294 35.227 A 4.928 4.928 0 0 0 242.925 35.05 A 4.452 4.452 0 0 0 243.782 34.641 A 3.477 3.477 0 0 0 244.5 34.05 Q 245.1 33.4 245.325 32.525 A 9.024 9.024 0 0 0 245.561 31.173 A 10.583 10.583 0 0 0 245.6 30.65 L 245.6 10.75 L 252.9 10.75 L 252.9 42.55 L 245.6 42.55 L 245.6 41.75 Q 244.55 42.15 243.4 42.35 A 13.592 13.592 0 0 1 241.748 42.531 A 16.018 16.018 0 0 1 240.95 42.55 L 237.75 42.55 A 13.954 13.954 0 0 1 235.298 42.345 A 10.31 10.31 0 0 1 232.85 41.6 Q 230.75 40.65 229.375 39.125 Q 228 37.6 227.3 35.65 Q 226.6 33.7 226.6 31.65 L 226.6 10.75 L 233.85 10.75 L 233.85 30.2 A 12.188 12.188 0 0 0 233.918 31.516 A 10.035 10.035 0 0 0 234.025 32.25 A 3.676 3.676 0 0 0 234.476 33.475 A 3.442 3.442 0 0 0 234.775 33.9 Q 235.35 34.6 236.35 35 Q 237.35 35.4 239 35.4 Z M 319.5 35.4 L 320.9 35.4 A 11.289 11.289 0 0 0 321.898 35.359 Q 322.383 35.316 322.794 35.227 A 4.928 4.928 0 0 0 323.425 35.05 A 4.452 4.452 0 0 0 324.282 34.641 A 3.477 3.477 0 0 0 325 34.05 Q 325.6 33.4 325.825 32.525 A 9.024 9.024 0 0 0 326.061 31.173 A 10.583 10.583 0 0 0 326.1 30.65 L 326.1 10.75 L 333.4 10.75 L 333.4 42.55 L 326.1 42.55 L 326.1 41.75 Q 325.05 42.15 323.9 42.35 A 13.592 13.592 0 0 1 322.248 42.531 A 16.018 16.018 0 0 1 321.45 42.55 L 318.25 42.55 A 13.954 13.954 0 0 1 315.798 42.345 A 10.31 10.31 0 0 1 313.35 41.6 Q 311.25 40.65 309.875 39.125 Q 308.5 37.6 307.8 35.65 Q 307.1 33.7 307.1 31.65 L 307.1 10.75 L 314.35 10.75 L 314.35 30.2 A 12.188 12.188 0 0 0 314.418 31.516 A 10.035 10.035 0 0 0 314.525 32.25 A 3.676 3.676 0 0 0 314.976 33.475 A 3.442 3.442 0 0 0 315.275 33.9 Q 315.85 34.6 316.85 35 Q 317.85 35.4 319.5 35.4 Z M 362.8 10.75 L 350.15 53.4 L 343.25 53.4 L 346.45 42.45 L 336.8 10.75 L 343.75 10.75 L 349.85 31.05 L 355.85 10.75 L 362.8 10.75 Z M 174.6 42.55 L 174.6 23.2 L 163.8 0 L 171.9 0 L 178.45 13.55 L 178.85 13.55 Q 179.6 11.9 180.4 10.225 Q 181.2 8.55 182.05 6.8 L 185.3 0 L 193.35 0 L 182.2 23.25 L 182.2 42.55 L 174.6 42.55 Z M 85.5 31.75 L 85.5 22.05 Q 85.5 19.75 86.375 17.7 Q 87.25 15.65 88.7 14.1 Q 90.15 12.55 92 11.65 A 8.854 8.854 0 0 1 94.509 10.847 A 8.003 8.003 0 0 1 95.75 10.75 L 102.85 10.75 A 9.977 9.977 0 0 1 105.298 11.039 A 8.23 8.23 0 0 1 107.2 11.775 Q 109.1 12.8 110.4 14.4 Q 111.7 16 112.4 17.975 A 12.367 12.367 0 0 1 112.984 20.276 A 10.288 10.288 0 0 1 113.1 21.8 L 113.1 29.85 L 92.85 29.85 L 92.85 31.55 Q 92.85 33.8 94.125 34.725 Q 95.29 35.57 97.101 35.643 A 8.654 8.654 0 0 0 97.45 35.65 L 112 35.65 L 112 42.65 L 95.8 42.65 Q 93.7 42.65 91.825 41.825 Q 89.95 41 88.55 39.55 A 10.748 10.748 0 0 1 86.499 36.501 A 12.379 12.379 0 0 1 86.325 36.1 Q 85.5 34.1 85.5 31.75 Z M 302.8 10.4 L 302.8 13.85 Q 302.8 15.9 302 17.85 Q 301.2 19.8 299.8 21.25 L 299.85 21.25 A 8.107 8.107 0 0 1 301.837 23.291 A 7.51 7.51 0 0 1 302.525 24.575 Q 303.35 26.55 303.35 28.65 L 303.35 31.3 Q 303.35 33.95 302.6 36.05 A 10.987 10.987 0 0 1 301.532 38.261 A 9.229 9.229 0 0 1 300.5 39.6 Q 299.15 41.05 297.3 41.8 A 10.272 10.272 0 0 1 294.434 42.491 A 12.562 12.562 0 0 1 293.2 42.55 L 273.85 42.55 L 273.85 0 L 292.65 0 A 11.75 11.75 0 0 1 295.3 0.289 A 10.058 10.058 0 0 1 296.775 0.75 Q 298.65 1.5 300 2.875 A 9.268 9.268 0 0 1 301.97 5.907 A 10.707 10.707 0 0 1 302.075 6.175 Q 302.8 8.1 302.8 10.4 Z M 207.7 10.75 L 210.25 10.75 A 15.771 15.771 0 0 1 212.856 10.956 A 12.21 12.21 0 0 1 215.175 11.575 A 10.965 10.965 0 0 1 217.845 13.019 A 9.827 9.827 0 0 1 218.875 13.9 A 9.75 9.75 0 0 1 221.044 17.153 A 11.37 11.37 0 0 1 221.2 17.55 A 12.681 12.681 0 0 1 221.903 20.568 A 15.964 15.964 0 0 1 222 22.35 L 222 30.9 A 15.171 15.171 0 0 1 221.761 33.649 A 12.207 12.207 0 0 1 221.2 35.7 Q 220.4 37.85 218.875 39.375 A 10.174 10.174 0 0 1 215.709 41.508 A 11.889 11.889 0 0 1 215.175 41.725 A 12.473 12.473 0 0 1 212.389 42.414 A 16.204 16.204 0 0 1 210.25 42.55 L 207.7 42.55 A 15.262 15.262 0 0 1 204.979 42.317 A 12.178 12.178 0 0 1 202.825 41.725 A 10.69 10.69 0 0 1 200.048 40.188 A 9.745 9.745 0 0 1 199.125 39.375 A 10.031 10.031 0 0 1 196.903 35.966 A 11.572 11.572 0 0 1 196.8 35.7 A 12.681 12.681 0 0 1 196.097 32.682 A 15.964 15.964 0 0 1 196 30.9 L 196 22.35 A 15.171 15.171 0 0 1 196.239 19.601 A 12.207 12.207 0 0 1 196.8 17.55 A 10.147 10.147 0 0 1 198.366 14.743 A 9.37 9.37 0 0 1 199.125 13.9 A 10.292 10.292 0 0 1 202.161 11.849 A 12.118 12.118 0 0 1 202.825 11.575 A 12.599 12.599 0 0 1 205.827 10.857 A 15.971 15.971 0 0 1 207.7 10.75 Z M 210.25 17.9 L 207.7 17.9 Q 205.75 17.9 204.425 19.2 A 4.37 4.37 0 0 0 203.121 22.042 A 5.929 5.929 0 0 0 203.1 22.55 L 203.1 30.7 A 5.176 5.176 0 0 0 203.336 32.296 A 4.255 4.255 0 0 0 204.425 34.05 Q 205.75 35.35 207.7 35.35 L 210.25 35.35 A 5.034 5.034 0 0 0 211.892 35.092 A 4.286 4.286 0 0 0 213.55 34.05 A 4.383 4.383 0 0 0 214.818 31.322 A 5.953 5.953 0 0 0 214.85 30.7 L 214.85 22.55 A 5.272 5.272 0 0 0 214.621 20.961 A 4.268 4.268 0 0 0 213.55 19.2 A 4.391 4.391 0 0 0 210.619 17.912 A 5.865 5.865 0 0 0 210.25 17.9 Z M 296 30 L 296 29.55 Q 296 28.6 295.675 27.75 A 4.658 4.658 0 0 0 295.015 26.559 A 4.297 4.297 0 0 0 294.775 26.275 Q 294.2 25.65 293.425 25.275 Q 292.65 24.9 291.8 24.9 L 281.2 24.9 L 281.2 34.7 L 291.8 34.7 Q 292.65 34.7 293.425 34.325 Q 294.2 33.95 294.775 33.325 A 4.505 4.505 0 0 0 295.612 32.008 A 5.181 5.181 0 0 0 295.675 31.85 Q 296 31 296 30 Z M 281.2 7.75 L 281.2 17.7 L 291.3 17.7 Q 292.15 17.7 292.9 17.325 Q 293.65 16.95 294.225 16.325 A 4.505 4.505 0 0 0 295.062 15.008 A 5.181 5.181 0 0 0 295.125 14.85 Q 295.45 14 295.45 13.05 L 295.45 12.4 A 4.907 4.907 0 0 0 295.252 10.992 A 4.526 4.526 0 0 0 295.125 10.625 Q 294.8 9.8 294.225 9.15 Q 293.65 8.5 292.9 8.125 Q 292.15 7.75 291.3 7.75 L 281.2 7.75 Z M 92.95 23.6 L 92.95 23.95 L 105.85 23.95 L 105.85 23.6 A 7.596 7.596 0 0 0 105.632 21.734 A 5.687 5.687 0 0 0 104.6 19.6 A 3.976 3.976 0 0 0 101.707 18.02 A 5.165 5.165 0 0 0 101.25 18 L 97.35 18 A 3.819 3.819 0 0 0 96.206 18.167 A 3.401 3.401 0 0 0 95.55 18.45 Q 94.75 18.9 94.175 19.675 A 5.82 5.82 0 0 0 93.459 20.963 A 6.962 6.962 0 0 0 93.275 21.475 Q 92.95 22.5 92.95 23.6 Z",
  },
  animate: { pathLength: 1, transition: { duration: 5 , repeat: Infinity } },
  exit: { pathLength: 0, transition: { duration: 10 } },
};
function Header() {
  return (
    <>
      <Logo viewBox="0 0 362.8 53.4">
        <motion.path
          variants={logoVariants}
          initial="initial"
          animate="animate"
          exit="exit"
        />
      </Logo>
    </>
  );
}
export default Header;
